# 🤖 Autonomous Vendor & Support Resolution Agent

**Agentic AI Hackathon — Tech Zephyr 4.0, IIT Bhubaneswar**

A single agentic system that handles two high-friction business workflows for an online retail business: **customer support tickets** and **vendor/procurement negotiation**. Built for the Agentic AI Hackathon at IIT Bhubaneswar.

---

## 📌 Problem

Two of the highest-friction, most repetitive workflows inside a growing business are customer support ticket resolution and vendor/procurement negotiation. Both are largely repetitive, but a meaningful minority of cases genuinely need judgment, negotiation, or escalation.

This agent handles both through one unified loop:

**Observe → Decide → Act → Evaluate → Adapt**

It classifies each incoming request, tries to resolve it autonomously using the right tool (knowledge-base search or vendor negotiation), evaluates whether the outcome is acceptable, and escalates to a human — with clear reasoning — when it isn't.

---

## ✅ Status

| Component | Status |
|---|---|
| Mock data (KB, vendor quotes, sample tickets) | ✅ Done |
| Evaluator criteria (`demo/evaluator_criteria.md`) | ✅ Done |
| Decision engine, tools, evaluator | ✅ Implemented & tested |
| Backend (`main.py`) — auto-resolve + escalation flows | ✅ Tested end-to-end |
| Problem & Solution Brief | ✅ Done |
| Architecture doc + diagram | ✅ Done |
| Streamlit UI (`ui/app.py`) | ⬜ In progress |
| Deployment | ⬜ Pending |
| Demo video | ⬜ Pending |

---

## 🏗️ Architecture

See [`demo/architecture.md`](demo/architecture.md) for the full diagram and explanation.

**Flow:**
```
Incoming request → Decision agent → Tool execution → Evaluate outcome → Auto-resolved | Escalate to human
```

Same loop for both domains — only the tool called in the "Act" step differs based on `request_type` (`support` or `vendor`).

---

## 📂 Project Structure

```
agentic-support-vendor/
├── main.py                    # FastAPI entry point
├── requirements.txt
├── .env.example
│
├── agent/
│   ├── decision_engine.py     # classifies request: simple / complex
│   ├── tools.py                # KB search + vendor negotiation logic
│   ├── evaluator.py            # checks if resolution is acceptable
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
│   └── app.py                  # Streamlit interface
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
git clone <repo-url>
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

### Test the full pipeline
In a second terminal, while the API is running:
```bash
curl.exe -X POST http://127.0.0.1:8000/process -H "Content-Type: application/json" -d "{\"request_id\": \"t001\", \"text\": \"I forgot my password, how do I reset it?\", \"request_type\": \"support\"}"
```

### Run the UI
```bash
streamlit run ui/app.py
```

---

## 👥 Who's Building What

| Member | Role | Responsibilities |
|---|---|---|
| **Vanshika Gupta** (MBA, AI & ML) | Business/Product | Problem brief, mock data (KB + vendor quotes), evaluator criteria, demo script |
| **Anshika Agarwal** (MBA, Tech & Finance) | Tech | Decision engine, tools, escalation logic, API + Streamlit wiring, deployment |

---

## 🔐 Environment Variables

See `.env.example`. Never commit your real `.env` file — it's already in `.gitignore`.

```
LLM_API_KEY=your_groq_api_key_here
LLM_PROVIDER=groq
```

---

## 🌿 Branching

- `main` — always working / demo-ready
- Work in feature branches (`feature/decision-engine`, `feature/ui`, etc.) and open a PR into `main` so the other person can review before merging.

---

## 📋 Hackathon Requirements Checklist (Round 1)

- [x] Problem & Solution Brief
- [x] System Architecture / Workflow diagram
- [ ] Source Code / GitHub Repository *(in progress — this repo)*
- [ ] 3–5 minute Demo Video
- [ ] Runnable or Deployed Version