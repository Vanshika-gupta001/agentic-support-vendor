"""
Tools the agent can call, based on request_type:
- "support": search knowledge_base.json for a matching answer
- "vendor": compare vendor_quotes.json and draft a counter-offer

TODO (Member 2):
- kb_search(text) -> reads data/knowledge_base.json, returns best match
- vendor_negotiate(text) -> reads data/vendor_quotes.json, drafts a
  counter-offer (can call the LLM to write the draft message)
"""

import json
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent / "data"


def kb_search(text: str) -> dict:
    # TODO: implement real matching (keyword or embedding based)
    with open(DATA_DIR / "knowledge_base.json") as f:
        kb = json.load(f)
    return {"matched": False, "answer": None, "kb_size": len(kb)}


def vendor_negotiate(text: str) -> dict:
    # TODO: implement quote comparison + counter-offer drafting
    with open(DATA_DIR / "vendor_quotes.json") as f:
        quotes = json.load(f)
    return {"counter_offer": None, "quotes_considered": len(quotes)}


def run_tool(classification: dict, text: str, request_type: str) -> dict:
    if request_type == "support":
        return kb_search(text)
    elif request_type == "vendor":
        return vendor_negotiate(text)
    raise ValueError(f"Unknown request_type: {request_type}")
