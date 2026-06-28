Generated `partner-targets.md` for **api-throttle**. (Note: the file held a stale roadmap for a different product, `mesh-sentry` — I overwrote it.)

Key decisions in the roadmap:

- **8 partners, two buckets** — *target APIs* we ship pre-built throttle profiles for (drives adoption/SEO) vs. *infra partners* with affiliate/rev-share (drives margin).
- **Revenue-first ordering:** Upstash (#2) is the only P0 with active rev-share (~25%) and becomes the *documented default distributed backend*, so its affiliate link rides every "scale to multiple workers" doc page.
- **Adoption hooks at zero cost:** OpenAI + Stripe + GitHub profiles make the README shareable and rank for "`<API>` rate limit python."
- **Reusable-abstraction leverage:** `RedisBackend` (built for Upstash) → Redis Cloud almost free; `cost-weighted limiter` (built for Shopify GraphQL points) → reusable for any credit-cost API.
- **Rev-share scorecard:** Tier-1 active (Upstash, Shopify, Redis Cloud, Sentry); Tier-2 credits-only (Twilio/SendGrid); Tier-0 adoption fuel (OpenAI, Stripe, GitHub).
- **PRD risk flags:** live-header vs. hardcoded limits, Stripe idempotency-safe retries, atomic distributed counters, and partner-program lead times.