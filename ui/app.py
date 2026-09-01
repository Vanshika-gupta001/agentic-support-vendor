"""
Streamlit UI: chat-style front end for the demo.

This gives judges (and us) a visual way to submit a request and watch the
agent's full Observe -> Decide -> Act -> Evaluate -> Adapt loop happen
step by step, instead of reading raw JSON in a terminal.
"""

import json
import sys
from pathlib import Path

import streamlit as st

# Make sure Python can find the "agent" package when this file is run
# directly with `streamlit run ui/app.py` (Streamlit runs from the ui/
# folder by default, so we add the project root to the import path).
sys.path.append(str(Path(__file__).parent.parent))

from agent.decision_engine import classify_request
from agent.tools import run_tool
from agent.evaluator import evaluate_outcome
from agent.escalation import escalate

# ---- Page setup ----
st.set_page_config(page_title="Agentic Resolution Demo", layout="centered")
st.title("🤖 Autonomous Vendor & Support Resolution Agent")
st.caption("Online retail business — one agent, two workflows: support tickets and vendor negotiation.")

# ---- Load sample tickets so judges can pick a ready-made example ----
DATA_DIR = Path(__file__).parent.parent / "data"
with open(DATA_DIR / "tickets_sample.json") as f:
    sample_tickets = json.load(f)

st.subheader("1. Enter a request")

# Let the user either pick a sample ticket or type their own
use_sample = st.checkbox("Use a sample ticket", value=True)

if use_sample:
    ticket_labels = [f"{t['request_id']} ({t['request_type']}): {t['text'][:60]}..." for t in sample_tickets]
    selected_label = st.selectbox("Choose a sample ticket", ticket_labels)
    selected_ticket = sample_tickets[ticket_labels.index(selected_label)]
    request_type = selected_ticket["request_type"]
    text = selected_ticket["text"]
    request_id = selected_ticket["request_id"]
    st.text_area("Request text", value=text, disabled=True)
else:
    request_type = st.selectbox("Request type", ["support", "vendor"])
    text = st.text_area("Request text", placeholder="Type the incoming request here...")
    request_id = "manual-request"

# ---- Process button ----
if st.button("▶ Process request", type="primary"):
    if not text.strip():
        st.warning("Please enter some request text first.")
    else:
        # Step 1: Decide
        with st.spinner("Classifying request..."):
            classification = classify_request(text, request_type)

        st.subheader("2. Decision agent")
        st.write(f"**Complexity:** `{classification['complexity']}`")
        st.write(f"**Reason:** {classification['reason']}")

        # Step 2: Act
        with st.spinner("Running tool..."):
            tool_result = run_tool(classification, text, request_type)

        st.subheader("3. Tool execution")
        if request_type == "support":
            if tool_result["matched"]:
                st.success(f"KB match found: **{tool_result['matched_entry']['topic']}**")
                st.write(tool_result["answer"])
            else:
                st.warning("No knowledge base match found.")
        else:  # vendor
            if tool_result["quote_found"]:
                quote = tool_result["quote"]
                st.write(f"**Vendor:** {quote['vendor_name']}")
                st.write(f"**Item:** {quote['item']}")
                st.write(f"**Quoted price:** ₹{quote['quoted_price']:,}")
                st.write(f"**Our target price:** ₹{quote['threshold_price']:,}")
                st.info(tool_result["counter_offer_text"])
            else:
                st.warning("No matching vendor quote found.")

        # Step 3: Evaluate
        evaluation = evaluate_outcome(tool_result, request_type)

        st.subheader("4. Evaluation")
        if evaluation["accepted"]:
            st.success(f"✅ Accepted — reason: `{evaluation['reason']}`")
        else:
            st.error(f"❌ Not accepted — reason: `{evaluation['reason']}`")

        # Step 4: Adapt (escalate if needed)
        st.subheader("5. Outcome")
        if evaluation["accepted"]:
            st.success("🎉 **Auto-resolved** — no human needed.")
        else:
            escalation_entry = escalate(request_id, text, tool_result, evaluation)
            st.error("🚨 **Escalated to human** — with reasoning logged below.")
            st.json(escalation_entry)

st.divider()
st.caption("Decision log is saved to `logs/decisions.log` for every escalation.")