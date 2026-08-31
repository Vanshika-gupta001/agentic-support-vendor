# Architecture

Business context: a single agent serving an online retail business —
handling customer support tickets (orders, refunds, delivery) and vendor
procurement negotiation (packaging, logistics, warehousing supplies).
Incoming request (support ticket or vendor query)
|
v
Decision agent — classifies: simple or complex
|
v
Tool execution — KB search (support) or vendor negotiation (procurement)
|
v
Evaluate outcome — is the resolution acceptable?
|
+----+----+
| |
v v

Same loop for both domains: **Observe → Decide → Act → Evaluate → Adapt.**
Only the tool called in the "Act" step differs based on `request_type`.

## Acceptance rules (see `demo/evaluator_criteria.md` for full detail)
- **Support:** accepted only if a real keyword match is found in the
  knowledge base and the request is actually about our store/order/account
- **Vendor:** accepted only if `quoted_price <= threshold_price * 1.05`
  (within a 5% auto-approve buffer)

## Why this counts as agentic, not a chatbot
- The agent chooses which tool to call based on the request (dynamic action
  selection)
- It evaluates its own output against a real threshold before responding
  (evaluation, not just generation)
- When the outcome fails evaluation, it changes course and escalates with
  explicit reasoning instead of returning a wrong or overconfident answer
  (adaptation)

![merged_agent_architecture.png](C:merged_agent_architecture.png)