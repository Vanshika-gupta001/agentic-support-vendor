"""
FastAPI entry point.
Wires together: decision_engine -> tools -> evaluator -> escalation.
"""

from fastapi import FastAPI
from pydantic import BaseModel

from agent.decision_engine import classify_request
from agent.tools import run_tool
from agent.evaluator import evaluate_outcome
from agent.escalation import escalate

app = FastAPI(title="Autonomous Vendor & Support Resolution Agent")


class RequestIn(BaseModel):
    request_id: str
    text: str
    request_type: str  # "support" or "vendor"


@app.post("/process")
def process_request(payload: RequestIn):
    # 1. Decide
    classification = classify_request(payload.text, payload.request_type)

    # 2. Act
    tool_result = run_tool(classification, payload.text, payload.request_type)

    # 3. Evaluate
    evaluation = evaluate_outcome(tool_result, payload.request_type)

    # 4. Adapt (escalate if needed)
    if not evaluation["accepted"]:
        return escalate(payload.request_id, payload.text, tool_result, evaluation)

    return {
        "request_id": payload.request_id,
        "status": "auto_resolved",
        "result": tool_result,
        "evaluation": evaluation,
    }


@app.get("/")
def health():
    return {"status": "ok"}
