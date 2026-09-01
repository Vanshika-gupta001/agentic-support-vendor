
## Setup (both members — run this first)

```bash
git clone <repo-url>
cd agentic-support-vendor
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env          # then add your Groq API key inside .env
```

This project uses **Groq's free API** (no credit card required) for the
LLM calls. Get a free key at [console.groq.com](https://console.groq.com)
and paste it into your `.env` file as `LLM_API_KEY`.

Run the API:
```bash
uvicorn main:app --reload
```

Test the full pipeline (in a second terminal, while the API is running):
```bash
curl.exe -X POST http://127.0.0.1:8000/process -H "Content-Type: application/json" -d "{\"request_id\": \"t001\", \"text\": \"I forgot my password, how do I reset it?\", \"request_type\": \"support\"}"
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