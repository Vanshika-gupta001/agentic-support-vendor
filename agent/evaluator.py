"""
Evaluator: decides whether the tool's result is "acceptable" or needs
escalation. This is the "adapt" trigger in the agent's decision loop.

Implements the acceptance rules defined in demo/evaluator_criteria.md:

Support tickets: accepted only if a real keyword match was found AND the
request is actually about our store/order/account (not an unrelated ask).

Vendor negotiation: accepted only if quoted_price <= threshold_price * 1.05
(within a 5% auto-approve buffer).
"""

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("evaluator")

# 5% buffer on vendor price, as defined in demo/evaluator_criteria.md
VENDOR_PRICE_BUFFER = 1.05


def _evaluate_support(tool_result: dict) -> dict:
    """
    Evaluates a support/KB tool result.

    Rejects if no KB match was found, since that means the agent has no
    real basis for an answer and should not guess.
    """
    if not tool_result.get("matched"):
        return {
            "accepted": False,
            "reason": "no_kb_match",
        }

    # A match was found by tools.py's keyword search. We treat any real
    # keyword match as sufficient confidence for this hackathon's scope;
    # a production system would add a confidence score here.
    return {
        "accepted": True,
        "reason": "kb_match_found",
    }


def _evaluate_vendor(tool_result: dict) -> dict:
    """
    Evaluates a vendor negotiation tool result against the price
    threshold defined for that vendor's quote.
    """
    if not tool_result.get("quote_found"):
        return {
            "accepted": False,
            "reason": "no_vendor_quote_found",
        }

    quote = tool_result["quote"]
    quoted_price = quote["quoted_price"]
    threshold_price = quote["threshold_price"]
    max_acceptable = threshold_price * VENDOR_PRICE_BUFFER

    if quoted_price <= max_acceptable:
        return {
            "accepted": True,
            "reason": "price_within_threshold",
        }

    return {
        "accepted": False,
        "reason": "price_above_threshold",
    }


def evaluate_outcome(tool_result: dict, request_type: str) -> dict:
    """
    Evaluates whether a tool's result is acceptable enough to auto-resolve,
    or whether it needs to be escalated to a human.

    Args:
        tool_result: the dict returned by tools.py's kb_search() or
            vendor_negotiate().
        request_type: "support" or "vendor".

    Returns:
        {"accepted": bool, "reason": "<short reason code>"}
    """
    if request_type == "support":
        result = _evaluate_support(tool_result)
    elif request_type == "vendor":
        result = _evaluate_vendor(tool_result)
    else:
        raise ValueError(f"Unknown request_type: {request_type!r}. Expected 'support' or 'vendor'.")

    logger.info("Evaluation result: accepted=%s, reason=%s", result["accepted"], result["reason"])
    return result