Generated `/tmp/breakeven.md` for **api-throttle**.

Key decisions baked into the model:

- **Open-core framing** — the Python library is free (that's the only credible model for a dev rate-limiting lib; you can't paywall `pip install`). Revenue comes from a hosted **distributed quota coordination service** — the pain that forces an upgrade is needing *shared* rate-limit state across workers/regions, which you can't get from an in-process library.
- **COGS ≈ $3.34/acct/mo** — low, because OSS self-hosters cost ~$0 and the hosted layer is thin (Redis counters + decision RPC). ~93% gross margin at the $49 tier.
- **Tiers:** Free → Pro $49 → Scale $249 → Enterprise from $1.5K. Pro is the wedge.
- **CAC ~$150 blended** (OSS funnel does the heavy lifting), **LTV ~$2,008**, → **13:1**, ~2.1mo payback.
- **Break-even: ~34 accounts** (lean) / **~114** with one salary.
- **$10K MRR: ~150 Pro + 11 Scale = 161 accounts**, ~9–12 months from an OSS launch.

The headline risk I flagged: quota *correctness* — if the service ever lets a customer breach a third-party limit and get their API key banned, trust dies. That, not acquisition, is where the first $10K MRR of effort should go.