# Architecture

**Problem statement alignment:** Track 3 — Smart Automation, Problem
Statement 5: Autonomous Customer Resolution Agent.

Business context: a single agent serving an online retail business —
handling customer support tickets (orders, refunds, delivery) by
actually resolving them (not just answering), plus vendor procurement
negotiation as an additional capability.

## Flow

1. **Incoming request** — support ticket or vendor query
2. **Decision agent** — classifies the request as simple or complex
3. **Tool execution** — KB search + action execution (support) or vendor negotiation (procurement)
4. **Verify** — checks if the action actually completed, or was blocked by a system constraint
5. **Evaluate outcome** — checks if the resolution is acceptable
6. **Outcome** — either **auto-resolved**, or **escalated to a human** with reasoning

Same loop for both domains: **Observe → Decide → Act → Verify → Evaluate → Adapt.**

For support requests, the agent doesn't just return an answer — it
executes a simulated state-changing action (e.g. issuing a replacement,
confirming a refund, cancelling an order) and verifies whether that
action actually succeeded. If the action is blocked by a simulated
business constraint (e.g. the order already shipped, so cancellation
isn't possible), the agent adapts by escalating to a human with the
exact block reason, instead of pretending the action worked.

## Diagram

![Architecture diagram](merged_agent_architecture.png)

## Acceptance rules (see `demo/evaluator_criteria.md` for full detail)
- **Support:** accepted only if a real keyword match is found, the request is
  actually about our store/order/account, AND the resulting action
  completed successfully (not blocked)
- **Vendor:** accepted only if `quoted_price <= threshold_price * 1.05`
  (within a 5% auto-approve buffer)

## Why this counts as agentic, not a chatbot
- The agent chooses which tool to call based on the request (dynamic action
  selection)
- It **executes a real state-changing action**, not just a text response
- It **verifies** the outcome of that action before declaring success
- It evaluates its own output against a real threshold before responding
- When the outcome fails evaluation (no match, blocked action, or price
  over threshold), it changes course and escalates with explicit
  reasoning instead of returning a wrong or overconfident answer
  (adaptation)