Generated `user-stories.md` for **api-throttle** — 14 stories across 4 epics:

- **Epic 1 — Core Rate Limiting**: declarative limiter, async-native, pluggable algorithms (token/leaky/window), weighted cost.
- **Epic 2 — Resilience & Server-Aware Adaptation**: retry+backoff, `X-RateLimit` header self-tuning, circuit breaker.
- **Epic 3 — Distributed & Multi-Tenant**: shared Redis backend, per-key/tenant limits, clock-skew tolerance.
- **Epic 4 — DX & Observability**: drop-in `requests`/`httpx`/`aiohttp` adapters, metrics hooks, introspection/dry-run, typed API.

Each story has Connextra phrasing, 3–5 acceptance criteria, and S/M/L sizing. I added a coverage table and an opinionated MVP cut.

**Key strategic call baked in:** the defensible/paid wedge is **Epic 3 (distributed shared-state limiting) + US-2.2 (server-signaled adaptation)** — a single-process token bucket is a 30-line gist anyone can copy, but *correct global quota enforcement across N workers* is the thing teams can't trivially DIY. That's where this product earns willingness-to-pay rather than just GitHub stars. Worth flagging to validation/PM: confirm that distributed correctness (not just convenience) is the actual budget-holding pain before over-investing in Epics 1–2.