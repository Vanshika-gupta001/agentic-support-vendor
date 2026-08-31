"""
Decision engine: classifies an incoming request as "simple" (agent can
resolve on its own) or "complex" (needs negotiation / will likely need
escalation).

TODO (Member 2):
- Call the LLM with the request text + request_type
- Return a dict like: {"complexity": "simple" | "complex", "reason": "..."}
- Keep the prompt short and log the raw LLM reasoning for the demo video
"""


def classify_request(text: str, request_type: str) -> dict:
    # TODO: replace with real LLM call
    return {
        "complexity": "simple",
        "reason": "placeholder - not yet implemented",
    }
