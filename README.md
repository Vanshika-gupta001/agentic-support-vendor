# Autonomous Vendor & Support Resolution Agent

Agentic AI Hackathon — Tech Zephyr 4.0, IIT Bhubaneswar

## Problem
A single agentic system that handles two high-friction business workflows:
1. Customer support tickets
2. Vendor / procurement negotiation requests

Both follow the same loop: **Observe → Decide → Act → Evaluate → Adapt**.
The agent classifies an incoming request, tries to resolve it autonomously
using the right tool (knowledge-base search or vendor negotiation), evaluates
whether the outcome is acceptable, and escalates to a human with clear
reasoning if it isn't.

## Architecture
See `demo/architecture.md` for the diagram and explanation.

Flow: `Incoming request → Decision agent → Tool execution → Evaluate outcome → (Auto-resolved | Escalate to human)`

## Project structure
```
agentic-support-vendor/
├── main.py                 # FastAPI entry point
├── agent/
│   ├── decision_engine.py  # classifies request: simple / complex
│   ├── tools.py            # KB search + vendor negotiation logic
│   ├── evaluator.py        # checks if resolution is acceptable
│   └── escalation.py       # handles handoff + reasoning log
├── data/
│   ├── knowledge_base.json # mock support KB
│   ├── vendor_quotes.json  # mock vendor data
│   └── tickets_sample.json # sample incoming requests for demo
├── logs/
│   └── decisions.log       # agent's decision trail (for demo + judges)
├── ui/
│   └── app.py               # Streamlit interface
└── demo/
    ├── demo_script.md       # script for the 3-5 min video
    └── architecture.md      # architecture diagram + explanation
```

## Setup (both members — run this first)

```bash
git clone <repo-url>
cd agentic-support-vendor
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env          # then add your LLM API key inside .env
```

Run the API:
```bash
uvicorn main:app --reload
```

Run the UI:
```bash
streamlit run ui/app.py
```

## Who's building what
- **Vanshika Gupta (MBA, AI & ML) — business/product side:** problem brief,
  mock data (KB + vendor quotes), evaluator criteria, demo script
- **Anshika Agarwal (MBA, Tech & Finance) — tech side:** decision engine, tools, escalation
  logic, API + Streamlit wiring, deployment

## Environment variables
See `.env.example`. Never commit your real `.env` file — it's already in
`.gitignore`.

## Branching
- `main` — always working/demo-ready
- Work in feature branches (`feature/decision-engine`, `feature/ui`, etc.)
  and open a PR into `main` so the other person can review before merging.
