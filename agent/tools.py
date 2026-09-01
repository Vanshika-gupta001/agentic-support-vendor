"""
Tools the agent can call, based on request_type:
- "support": search knowledge_base.json for a matching answer
- "vendor": compare vendor_quotes.json and draft a counter-offer

Uses Groq's free API (OpenAI-compatible) for the parts that need an LLM
(drafting the vendor counter-offer message).
"""

import os
import json
import logging
from pathlib import Path
from dotenv import load_dotenv
from groq import Groq

load_dotenv()  # reads .env file so LLM_API_KEY is available even when this module is imported directly

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("tools")

client = Groq(api_key=os.getenv("LLM_API_KEY"))
MODEL_NAME = "openai/gpt-oss-120b"

DATA_DIR = Path(__file__).parent.parent / "data"


def _load_json(filename: str) -> list:
    """Small helper to load a JSON file from the data directory."""
    with open(DATA_DIR / filename) as f:
        return json.load(f)


def kb_search(text: str) -> dict:
    """
    Searches the knowledge base for a matching entry using simple keyword
    matching. This is intentionally simple (no embeddings/vector search
    needed) since the hackathon rules explicitly say vector databases and
    RAG pipelines are not mandatory.

    Returns:
        {
            "matched": bool,
            "matched_entry": dict | None,
            "answer": str | None,
        }
    """
    kb = _load_json("knowledge_base.json")
    text_lower = text.lower()

    best_match = None
    best_match_count = 0

    for entry in kb:
        keywords = entry.get("keywords", [])
        match_count = sum(1 for kw in keywords if kw.lower() in text_lower)
        if match_count > best_match_count:
            best_match_count = match_count
            best_match = entry

    if best_match is not None:
        logger.info("KB match found: '%s' (%d keyword hits)", best_match["topic"], best_match_count)
        return {
            "matched": True,
            "matched_entry": best_match,
            "answer": best_match["answer"],
        }

    logger.info("No KB match found for request text.")
    return {
        "matched": False,
        "matched_entry": None,
        "answer": None,
    }


def _find_vendor_quote(text: str, quotes: list) -> dict | None:
    """
    Finds the vendor quote entry that best matches the request text, by
    checking if the vendor name or item description appears in the text.
    """
    text_lower = text.lower()
    for quote in quotes:
        if quote["vendor_name"].lower() in text_lower or quote["item"].lower() in text_lower:
            return quote
    return None


def _draft_counter_offer(quote: dict) -> str:
    """
    Uses the LLM to draft a short, professional counter-offer message
    based on the quoted price and our threshold price.
    """
    prompt = f"""Draft a short, professional counter-offer email to a vendor.

Vendor: {quote['vendor_name']}
Item: {quote['item']}
Their quoted price: {quote['quoted_price']}
Our target price: {quote['threshold_price']}

Keep it under 80 words. Be polite but direct. Propose our target price
and ask if they can match it or meet in the middle.
"""
    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            max_tokens=200,
            messages=[{"role": "user", "content": prompt}],
        )
        return response.choices[0].message.content.strip()
    except Exception as exc:
        logger.error("LLM call failed while drafting counter-offer: %s", exc)
        return (
            f"Could not auto-draft a counter-offer ({exc.__class__.__name__}). "
            f"Manual negotiation needed for {quote['vendor_name']}."
        )


def vendor_negotiate(text: str) -> dict:
    """
    Finds the relevant vendor quote and drafts a counter-offer.

    Returns:
        {
            "quote_found": bool,
            "quote": dict | None,
            "counter_offer_text": str | None,
        }
    """
    quotes = _load_json("vendor_quotes.json")
    matched_quote = _find_vendor_quote(text, quotes)

    if matched_quote is None:
        logger.info("No matching vendor quote found for request text.")
        return {
            "quote_found": False,
            "quote": None,
            "counter_offer_text": None,
        }

    counter_offer_text = _draft_counter_offer(matched_quote)
    logger.info("Drafted counter-offer for vendor '%s'", matched_quote["vendor_name"])

    return {
        "quote_found": True,
        "quote": matched_quote,
        "counter_offer_text": counter_offer_text,
    }


def run_tool(classification: dict, text: str, request_type: str) -> dict:
    """
    Routes to the correct tool based on request_type.

    Note: `classification` (from decision_engine.py) is accepted here for
    future use (e.g. skipping tool execution entirely for very simple
    cases) but is not required by the current tool implementations.
    """
    if request_type == "support":
        return kb_search(text)
    elif request_type == "vendor":
        return vendor_negotiate(text)
    raise ValueError(f"Unknown request_type: {request_type!r}. Expected 'support' or 'vendor'.")