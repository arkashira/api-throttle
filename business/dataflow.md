# Dataflow Architecture — `api-throttle`

> Scope: `api-throttle` is an embedded Python library, so the "system" is the host application process plus an optional shared coordination store. The dataflow below traces a single outbound third-party API call from the moment app code requests a token through to the response handed back, including the distributed-state path that makes limits correct across N worker processes.

## ASCII Block Diagram

```
                         ┌─── AUTH BOUNDARY: in-process (no network) ───┐
 EXTERNAL                │                                              │
 ┌──────────────┐        │  ┌────────────────────────────────────┐     │
 │ Third-party  │        │  │  INGESTION                          │     │
 │ APIs         │───┐    │  │  • @throttle decorator / context mgr │     │
 │ (Stripe,     │   │    │  │  • acquire(key, cost) call           │     │
 │  OpenAI,     │   │    │  │  • 429 / Retry-After sniffer         │     │
 │  GitHub…)    │   │    │  └──────────────┬─────────────────────┘     │
 │ + their      │   │    │                 │ token request              │
 │ rate-limit   │   │    │                 ▼                            │
 │ headers      │   │    │  ┌────────────────────────────────────┐     │
 └──────┬───────┘   │    │  │  PROCESSING / TRANSFORM             │     │
        │           │    │  │  • Algorithm engine                 │     │
        │ HTTP resp │    │  │    (token-bucket / sliding-window /  │     │
        │ (headers, │    │  │     GCRA / leaky-bucket)            │     │
        │  429s)    │    │  │  • Cost weighting + key resolution  │     │
        │           │    │  │  • Adaptive backoff (header-driven) │     │
        │           │    │  └───────┬──────────────────┬─────────┘     │
        │           │    │          │ local fast-path  │ shared state   │
        │           │    │          ▼                  ▼                │
        │           │    │  ┌──────────────┐   ╎  AUTH BOUNDARY: ╎      │
        │           │    │  │ STORAGE      │   ╎  network +TLS  ╎       │
        │           │    │  │ • in-mem     │   ╎  +ACL          ╎       │
        │           │    │  │   (asyncio/  │   ▼                        │
        │           │    │  │    thread    │  ┌─────────────────────┐   │
        │           │    │  │    lock)     │  │ Redis / Memcached   │   │
        │           │    │  └──────┬───────┘  │ (Lua CAS counters)  │   │
        │           │    │         │          └─────────┬───────────┘   │
        │           │    │         ▼                    ▼               │
        │           │    │  ┌────────────────────────────────────┐     │
        │           │    │  │  QUERY / SERVING                    │     │
        │           │    │  │  • allow / deny / wait(t) verdict   │     │
        │           │    │  │  • remaining / reset introspection  │     │
        │           │    │  │  • metrics emit (Prometheus/OTel)   │     │
        │           │    │  └──────────────┬─────────────────────┘     │
        │           │    │                 │ verdict                    │
        │           │    └─────────────────┼────────────────────────────┘
        │           │                      ▼
        │           │              ┌────────────────┐
        └───────────┴──────────────│  EGRESS        │
              actual API call      │  • caller code │
              fired only on ALLOW  │  • async/sync  │
                                   │    return      │
                                   └────────────────┘
```

## External Data Sources
- **Third-party API responses** — the authoritative ground truth. Status codes (`429`, `503`) and `Retry-After`, `X-RateLimit-Remaining`, `X-RateLimit-Reset`, `RateLimit-*` (IETF draft) headers feed the adaptive layer.
- **Caller-supplied limit config** — declarative policies (`100/min`, `5000/hour`, per-endpoint, per-tenant) from code, env vars, or a YAML/TOML file loaded at init.
- **Wall clock** — monotonic clock (`time.monotonic()`) for local windows; server-side `TIME` in Redis Lua to avoid client clock skew across nodes.
- **Auth boundary:** none of these cross a trust boundary the library controls — credentials for the third-party API live in the *caller's* code, never in `api-throttle`. The library must never log or persist the API payload or auth headers (PII/secret-leak risk).

## Ingestion Layer
- **`@throttle(key=..., rate=...)` decorator** and **`async with limiter.acquire(key, cost=1):` context manager** — the two primary entry points.
- **Low-level `acquire()` / `try_acquire()` / `wait_for_token()`** API for manual control.
- **Response-header sniffer** — optional middleware/hook (e.g. `httpx` event hook, `requests` adapter) that parses `429`/`Retry-After` from the *previous* call and feeds it back into processing.
- **Auth boundary:** purely in-process function calls. No deserialization of untrusted network input here except the third-party's own response headers, which are validated/clamped (reject negative or absurd `Retry-After`).

## Processing / Transform Layer
- **Algorithm engine** — pluggable strategy: `TokenBucket` (default, burst-friendly), `SlidingWindowLog` (exact, memory-heavy), `SlidingWindowCounter` (approximate, cheap), `GCRA`/leaky-bucket (smoothest pacing). Target verdict latency: **< 50 µs local, < 1 ms Redis round-trip**.
- **Key resolver** — composes the rate-limit key (`{tenant}:{endpoint}:{method}`) and resolves cost weight (a bulk call may cost 10 tokens).
- **Adaptive backoff** — when the upstream returns `429`/`Retry-After`, dynamically tightens the local limit (multiplicative decrease) and recovers (additive increase) — keeps the app *under* the real ceiling without hammering.
- **Concurrency control** — `asyncio.Lock` / `threading.Lock` for in-process; atomic compare-and-set via a single **Redis Lua script** to make the read-modify-write of the counter race-free across processes.

## Storage Tier
- **In-memory (default)** — per-process dict of bucket states behind a lock. Zero deps, but limits are *per-process* (N workers ⇒ N× the intended rate). Fine for single-process tools/CLIs.
- **Redis (recommended for distributed)** — shared counters/buckets keyed with TTL = window size; updated atomically via Lua. One source of truth for a fleet of workers. Memcached supported as a lighter alternative (CAS-based, no Lua).
- **Schema:** `key → {tokens: float, last_refill: ts}` for token-bucket; sorted-set of timestamps for sliding-window-log. TTLs auto-expire idle keys to bound memory.
- **Auth boundary (critical):** the Redis hop crosses the network. Library must support **TLS (`rediss://`), AUTH password / ACL user, and a dedicated keyspace prefix** so a shared Redis can't be polluted or read by other tenants. Never store request payloads — only counters/timestamps.

## Query / Serving Layer
- **Verdict API** — returns `Allow`, `Deny`, or `RetryAfter(seconds)` so the caller can choose to block, raise, or queue.
- **Introspection** — `limiter.remaining(key)`, `.reset_at(key)`, `.peek()` for dashboards and pre-flight checks without consuming a token.
- **Observability egress** — optional Prometheus counters (`throttle_allowed_total`, `throttle_denied_total`, `throttle_wait_seconds`) and OpenTelemetry spans. **Opt-in only**; emits metric labels, never keys containing PII.
- **Auth boundary:** metrics scrape endpoint, if exposed, is the *caller's* responsibility to protect — library documents this and never opens a listening socket itself.

## Egress to User
- **Synchronous path:** `acquire()` either returns immediately (allow), sleeps until a token is available (`wait`), or raises `RateLimitExceeded` (fail-fast) — caller-selectable policy.
- **Async path:** `await limiter.acquire()` yields control to the event loop while waiting, so a single worker can pace thousands of coroutines without blocking.
- **Net effect:** the actual outbound third-party HTTP call fires *only* after an `Allow` verdict, keeping the application provably under the upstream's published ceiling and eliminating the `429`-retry-storm failure mode.
- **Auth boundary:** verdict and exceptions stay in-process; no trust boundary crossed on return.