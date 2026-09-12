# ⚡ Team AgentForge — Autonomous Vendor & Support Resolution Agent

**Agentic AI Hackathon — Tech Zephyr 4.0, IIT Bhubaneswar**

A single agentic system that handles two high-friction business workflows for an online retail business: **customer support tickets** and **vendor/procurement negotiation**.

🔗 **Live app:** [https://agentic-support-vendor-upx3udgmw5weges7qt7bbu.streamlit.app/]

📦 **GitHub:** github.com/Vanshika-gupta001/agentic-support-vendor

**Problem statement alignment:** Track 3 — Smart Automation, Problem Statement 5: Autonomous Customer Resolution Agent.

---

## 📌 Problem

Two of the highest-friction, most repetitive workflows inside a growing business are customer support ticket resolution and vendor/procurement negotiation. Both are largely repetitive, but a meaningful minority of cases genuinely need judgment, negotiation, or escalation.

This agent handles both through one unified loop:

**Observe → Decide → Act → Verify → Evaluate → Adapt**

It classifies each incoming request, retrieves relevant context, executes a real simulated resolution action (not just a text reply), verifies whether that action actually completed, evaluates the outcome against policy, and escalates to a human — with clear reasoning — when it can't safely resolve the case.

---

## ✅ Status

| Component | Status |
|---|---|
| Mock data (KB, vendor quotes, sample tickets) | ✅ Done |
| Evaluator criteria (`demo/evaluator_criteria.md`) | ✅ Done |
| Decision engine, tools, action execution, evaluator | ✅ Implemented & tested |
| Action verification (blocked-action escalation) | ✅ Implemented & tested |
| Backend (`main.py`) — auto-resolve + escalation flows | ✅ Tested end-to-end |
| Problem & Solution Brief | ✅ Done |
| Architecture doc + diagram | ✅ Done |
| Streamlit dashboard UI (`ui/app.py`) | ✅ Done |
| Deployment (Streamlit Community Cloud) | ✅ Live |
| Presentation deck | ✅ Done |
| Demo video | ✅ Done |

---

## 🏗️ Architecture

See [`demo/architecture.md`](demo/architecture.md) for the full diagram and explanation.

**Flow:**
```
Incoming request → Decision agent → Tool execution (KB search + action) → Verify action → Evaluate outcome → Auto-resolved | Escalate to human
```

Same loop for both domains — only the tool called in the "Act" step differs based on `request_type` (`support` or `vendor`). For support requests, the agent executes a real simulated action (replacement, refund confirmation, cancellation) and verifies it actually succeeded — if it's blocked by a business constraint (e.g. order already shipped), the agent adapts by escalating instead of pretending it worked.

---

## 🖥️ UI

A dark, dashboard-style interface: sidebar for picking/writing a request and tracking live session stats, a command-center style overview (processed / auto-resolved / escalated / resolution rate), a live activity feed of past escalations, and a step-by-step pipeline view with decision, action, and outcome cards.

---

## 📂 Project Structure

```
agentic-support-vendor/
├── main.py                    # FastAPI entry point
├── requirements.txt
├── .env.example
├── .streamlit/
│   └── config.toml             # dark theme config
│
├── agent/
│   ├── decision_engine.py     # classifies request: simple / complex
│   ├── tools.py                # KB search, action execution, vendor negotiation
│   ├── evaluator.py            # checks if resolution/action is acceptable
│   └── escalation.py           # handles handoff + reasoning log
│
├── data/
│   ├── knowledge_base.json    # mock support KB (10 topics)
│   ├── vendor_quotes.json     # mock vendor data (8 vendors)
│   └── tickets_sample.json    # sample requests for demo/testing
│
├── logs/
│   └── decisions.log          # agent's decision trail (for demo + judges)
│
├── ui/
│   └── app.py                  # Streamlit dashboard interface
│
└── demo/
    ├── demo_script.md          # script for the 3-5 min video
    ├── architecture.md         # architecture diagram + explanation
    └── evaluator_criteria.md   # exact acceptance rules for the evaluator
```

---

## 🚀 Setup

This project uses **Groq's free API** (no credit card required) for LLM calls. Get a free key at [console.groq.com](https://console.groq.com).

```bash
git clone https://github.com/Vanshika-gupta001/agentic-support-vendor.git
cd agentic-support-vendor

python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate

pip install -r requirements.txt

cp .env.example .env          # then paste your Groq key into LLM_API_KEY
```

### Run the API
```bash
uvicorn main:app --reload
```

### Run the UI
```bash
streamlit run ui/app.py
```

---

## 👥 Team AgentForge

| Member | Role | Responsibilities |
|---|---|---|
| **Vanshika Gupta** (MBA, AI & ML) | Business/Product | Problem brief, mock data, evaluator criteria, demo script, presentation |
| **Anshika Agarwal** (MBA, Tech & Finance) | Tech | Decision engine, tools, escalation logic, API + Streamlit wiring, deployment, demo video |

---

## 🔐 Environment Variables

See `.env.example`. Never commit your real `.env` file — it's already in `.gitignore`. For the deployed version, the key is set via Streamlit Community Cloud's Secrets manager instead.

```
LLM_API_KEY=your_groq_api_key_here
LLM_PROVIDER=groq
```

---

## 📋 Hackathon Requirements Checklist (Round 1)

- [x] Problem & Solution Brief
- [x] System Architecture / Workflow diagram
- [x] Source Code / GitHub Repository
- [x] 3–5 minute Demo Video
- [x] Runnable or Deployed Version