"""
Decision engine.

Responsibility: given an incoming request, decide whether it is "simple"
(the agent should try to resolve it automatically) or "complex" (it will
likely need negotiation, judgment, or escalation to a human).

This is the first step of the agent's Observe -> Decide -> Act -> Evaluate
-> Adapt loop. The classification produced here determines which tool
gets called next in tools.py.
"""

import os
import json
import logging
from anthropic import Anthropic

# Set up basic logging so classification decisions can be inspected later
# (useful for the demo video and for debugging).
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("decision_engine")

# The Anthropic client reads the API key from the environment.
# Make sure LLM_API_KEY is set in your .env file before running this.
client = Anthropic(api_key=os.getenv("LLM_API_KEY"))

# Model used for classification. Kept as a constant so it's easy to swap
# later without touching the rest of the logic.
MODEL_NAME = "claude-sonnet-4-6"


def _build_prompt(text: str, request_type: str) -> str:
    """
    Builds the instruction prompt sent to the LLM.

    Kept as a separate function so the prompt can be tuned independently
    of the API-calling logic, and so it can be unit-tested or reused.
    """
    return f"""You are a request classifier for a business agent system.

The system handles two types of requests:
- "support": customer support tickets (orders, refunds, delivery, account issues)
- "vendor": vendor/procurement negotiation requests (price quotes, contracts)

Request type: {request_type}
Request text: "{text}"

Classify this request as either "simple" or "complex":
- "simple" = likely resolvable automatically. For support: a common
  question with a known, factual answer. For vendor: a quote that is
  likely already close to an acceptable price.
- "complex" = likely needs negotiation, judgment, or is outside the
  system's scope entirely (e.g. unrelated to the business).

Respond with ONLY valid JSON, no extra text, no markdown formatting,
in exactly this format:
{{"complexity": "simple", "reason": "short one-sentence explanation"}}
or
{{"complexity": "complex", "reason": "short one-sentence explanation"}}
"""


def _parse_llm_response(raw_text: str) -> dict:
    """
    Parses the LLM's raw text output into a Python dict.

    LLMs sometimes wrap JSON in markdown code fences even when told not
    to, so we strip those defensively before parsing. If parsing still
    fails, we fail safe by defaulting to "complex" -- an unclear request
    should be escalated, not silently treated as simple.
    """
    cleaned = raw_text.strip()
    cleaned = cleaned.replace("```json", "").replace("```", "").strip()

    try:
        result = json.loads(cleaned)
    except json.JSONDecodeError:
        logger.warning("Failed to parse LLM response as JSON: %s", raw_text)
        return {
            "complexity": "complex",
            "reason": "Could not parse classifier response; defaulting to complex for safety.",
        }

    # Defensive validation: make sure the expected keys exist and the
    # complexity value is one of the two allowed values.
    if result.get("complexity") not in ("simple", "complex"):
        logger.warning("Unexpected complexity value in LLM response: %s", result)
        result["complexity"] = "complex"
        result.setdefault("reason", "Unexpected classifier output; defaulting to complex.")

    return result


def classify_request(text: str, request_type: str) -> dict:
    """
    Classifies an incoming request as simple or complex.

    Args:
        text: the raw text of the incoming request.
        request_type: "support" or "vendor".

    Returns:
        A dict of the form:
        {"complexity": "simple" | "complex", "reason": "<explanation>"}
    """
    if request_type not in ("support", "vendor"):
        raise ValueError(f"Unknown request_type: {request_type!r}. Expected 'support' or 'vendor'.")

    prompt = _build_prompt(text, request_type)

    try:
        response = client.messages.create(
            model=MODEL_NAME,
            max_tokens=200,
            messages=[{"role": "user", "content": prompt}],
        )
    except Exception as exc:
        # If the API call itself fails (network issue, bad key, rate
        # limit, etc.), escalate rather than crash the whole pipeline.
        logger.error("LLM call failed during classification: %s", exc)
        return {
            "complexity": "complex",
            "reason": f"Classifier call failed ({exc.__class__.__name__}); defaulting to complex.",
        }

    raw_text = response.content[0].text
    result = _parse_llm_response(raw_text)

    logger.info(
        "Classified request as '%s' (reason: %s)",
        result["complexity"],
        result["reason"],
    )

    return result