"""
Escalation: when the evaluator rejects the outcome, generate a clear
"why" reasoning and log it. This log is what you show judges in the demo
to prove the agent adapts instead of failing silently.

TODO (Member 2):
- Write structured entries to logs/decisions.log (JSON lines are easiest)
"""

import json
from datetime import datetime
from pathlib import Path

LOG_PATH = Path(__file__).parent.parent / "logs" / "decisions.log"


def escalate(request_id: str, text: str, tool_result: dict, evaluation: dict) -> dict:
    entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "request_id": request_id,
        "status": "escalated",
        "reason": evaluation.get("reason"),
        "tool_result": tool_result,
    }

    LOG_PATH.parent.mkdir(exist_ok=True)
    with open(LOG_PATH, "a") as f:
        f.write(json.dumps(entry) + "\n")

    return entry
