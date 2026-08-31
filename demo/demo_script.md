# Demo video script (3-5 min)

Business context: an online retail store using one agent to handle both
customer support tickets and vendor/procurement negotiation.

## 1. Intro (20s)
- "Support and procurement teams spend most of their time on repetitive
  requests, but a small share genuinely need judgment. We built one agent
  that resolves what it can and escalates what it can't — with reasoning."
- Show the architecture diagram briefly (Incoming request → Decision agent
  → Tool execution → Evaluate → Auto-resolved / Escalate).

## 2. Case 1 — support, auto-resolved (45-60s)
- Use ticket `t001`: "I forgot my password, how do I reset it?"
- Show: Decision agent classifies as simple → KB search finds `kb001` →
  Evaluator accepts (clear keyword match) → response returned instantly.
- Say out loud what the agent decided and why at each step.

## 3. Case 2 — vendor, escalated on price (45-60s)
- Use ticket `t004`: "National Freight Carriers quoted 600000 for the
  quarterly freight contract, negotiate it down."
- Threshold price is 540000; 600000 is well above the 5% auto-approve
  buffer → Evaluator rejects → Escalation triggered.
- Show the escalation log entry with the reasoning ("price_above_threshold")
  — this is the "why", not just a failure.

## 4. Adaptation moment — off-topic request (30-40s)
- Use ticket `t006`: an unrelated question (stock market advice) sent to
  support.
- Show the agent correctly refusing to fabricate a KB answer and instead
  escalating with reason `"out_of_scope"`.
- This is the key "adapts instead of breaking" moment — call it out
  explicitly on camera.

## 5. Wrap-up (20s)
- Recap: one agent, two workflows, same decide → act → evaluate → adapt
  loop.
- Mention the deployed link and GitHub repo (show on screen).

## Recording checklist
- Record screen at 1080p, keep mouse movements slow and deliberate
- Narrate every decision the agent makes — don't just click through silently
- Keep total runtime between 3-5 minutes (practice once before recording)