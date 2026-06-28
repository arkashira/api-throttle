Generated `/tmp/tech-spec.md` for **api-throttle**.

Key opinionated calls in this v1 spec:

- **Stdlib-only core, zero forced deps** — the library installs with nothing extra; Redis/httpx/server are optional extras. This is the adoption lever for a DX product.
- **Library-first, control plane optional** — `mode="managed"` gates any network dependency; default is purely client-side (in-memory or local Redis), so it works offline and self-hosted.
- **`/v1/check` as the single hot path** — atomic Lua-backed token-bucket on Redis, designed to short-circuit locally when not in managed mode.
- **Free-tier hosting ≈ $0/mo at 0–50 orgs** (Fly scale-to-zero + Upstash Redis + Supabase Postgres).
- **Hard quality bars** appropriate for a library: `mypy --strict`, ≥90% coverage, a `<5 µs` per-`acquire()` perf gate, signed wheels via PyPI OIDC.

One thing worth flagging for the next section: the control plane bolts a hosted/monetizable surface onto what BD framed as "a Python library." If the business model is pure OSS library (no managed plane), sections 2/4/6 collapse significantly — worth confirming the monetization intent before the pricing/GTM pack.