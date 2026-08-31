# Evaluator criteria

These are the acceptance rules the agent uses to decide "accepted" vs
"escalate". Anshika: implement these directly inside `agent/evaluator.py`.

## Support tickets

A KB-based resolution is **accepted** only if ALL of these are true:
- A keyword match was found in `knowledge_base.json` (at least one keyword
  from the entry appears in the request text)
- The matched topic is clearly relevant to the request (not a vague/partial
  match)
- The request is actually about our store/order/account — not an unrelated
  or off-topic ask (see `t006` in `tickets_sample.json` for this case)

Otherwise → **escalate**, with reason:
- `"no_kb_match"` — nothing matched
- `"out_of_scope"` — request isn't about our business at all
- `"low_confidence"` — a match exists but it's weak/ambiguous

## Vendor negotiation

A counter-offer is **accepted** only if:
- `quoted_price <= threshold_price * 1.05` (i.e. within 5% of our target —
  we can auto-approve without a human)

Otherwise → **escalate**, with reason:
- `"price_above_threshold"` — quote is more than 5% over what we're willing
  to auto-approve; a human should review or continue negotiating

## Why these numbers

- 5% buffer on vendor price = reasonable auto-approval margin without
  needing a human for every small gap
- KB matching stays conservative (real keyword match required) so the agent
  never confidently answers something it doesn't actually know — this is
  what we'll show in the demo as the "adaptation" moment (t006: an
  unrelated/off-topic request correctly gets escalated instead of the
  agent making up an answer)