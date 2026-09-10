# Demo video script (3-5 min)

Business context: an online retail store using one agent to handle both
customer support tickets and vendor/procurement negotiation. Recorded on
the deployed dashboard UI (sidebar for input, main area for the pipeline).

## Recording setup
- Use the **deployed link** (not localhost) so judges see the real, live app
- Screen recorder: Loom (free, browser-based, easiest) or OBS Studio
- Record at 1080p, full browser window
- Do a silent practice run once before recording audio
- Estimated runtime: ~3.5 minutes at normal speaking pace

---

## 1. Intro
**[Screen: Open the deployed app, show the header + sidebar]**

> "Hi, this is our project for the Agentic AI Hackathon — an autonomous
> agent for an online retail business. It handles two high-friction
> workflows: customer support tickets and vendor negotiation, through a
> single loop — Observe, Decide, Act, Evaluate, and Adapt."

---

## 2. Case 1 — Support, auto-resolved
**[Screen: Sidebar → select ticket t001 ("I forgot my password") → click "Process this ticket"]**

> "Let's start with a support ticket. The decision agent classifies this
> as simple. It searches our knowledge base, finds a matching answer, and
> the evaluator accepts it with high confidence. The request is
> auto-resolved — no human needed. You can see our session stats in the
> sidebar updating in real time."

---

## 3. Case 2 — Vendor, escalated on price
**[Screen: Select ticket t004 (National Freight Carriers) → click "Process this ticket"]**

> "Now a vendor negotiation case. The agent finds the matching quote — six
> lakh rupees — and drafts a counter-offer. But our evaluator checks it
> against a price threshold, and this quote is more than five percent over
> our target. So instead of accepting it blindly, the agent escalates to a
> human, with the exact reasoning logged."

**[Screen: Click "View full escalation log entry" to expand it]**

> "Here's that reasoning — fully transparent, so a human reviewer knows
> exactly why this needs their judgment."

---

## 4. Case 3 — Adaptation moment (off-topic request)
**[Screen: Select ticket t006 (off-topic stock market question) → click "Process this ticket"]**

> "This last case is important — it's a request that has nothing to do
> with our store at all. A simple chatbot might try to force an answer.
> Our agent recognizes this is out of scope and escalates instead of
> guessing. This is the adaptation behavior we wanted to demonstrate —
> the system knowing when *not* to act."

---

## 5. Wrap-up
**[Screen: Show sidebar stats one final time]**

> "So — one agent, two business workflows, one shared decide-evaluate-adapt
> loop. It's fully deployed and live at this link, and the complete source
> code is on GitHub. Thank you."

**[Screen: Show deployed URL and GitHub link clearly for a couple seconds before ending]**

---

## Recording checklist
- Narrate every decision out loud — don't just click silently
- Keep total runtime between 3-5 minutes (time yourself in a practice run)
- Speak a little slower than feels natural — nervousness speeds people up
- Pause 1-2 seconds after each click before speaking
- End cleanly on the wrap-up, don't trail off