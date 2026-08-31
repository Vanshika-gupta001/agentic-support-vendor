"""
Evaluator: decides whether the tool's result is "acceptable" or needs
escalation. This is the "adapt" trigger.

TODO (Member 1 defines criteria, Member 2 implements):
- support: was a confident KB match found?
- vendor: is the counter-offer within an acceptable price threshold?
"""


def evaluate_outcome(tool_result: dict, request_type: str) -> dict:
    # TODO: replace with real thresholds / confidence checks
    return {
        "accepted": False,
        "reason": "placeholder - evaluation logic not yet implemented",
    }
