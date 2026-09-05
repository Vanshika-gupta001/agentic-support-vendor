"""
Streamlit UI: dark, tech-startup-styled front end for the demo.

Shows the agent's full Observe -> Decide -> Act -> Evaluate -> Adapt loop
step by step. The dark theme itself comes from .streamlit/config.toml;
this file only adds a few extra styles (pills, quote boxes) tuned to
match that theme.
"""

import json
import sys
from pathlib import Path

import streamlit as st

sys.path.append(str(Path(__file__).parent.parent))

from agent.decision_engine import classify_request
from agent.tools import run_tool
from agent.evaluator import evaluate_outcome
from agent.escalation import escalate

# ---------------------------------------------------------------------------
# Page setup + dark-theme-matched styling
# ---------------------------------------------------------------------------
st.set_page_config(page_title="Resolution Agent", page_icon="⚡", layout="centered")

st.markdown("""
<style>
    .pill {
        display: inline-block;
        padding: 4px 14px;
        border-radius: 999px;
        font-size: 12px;
        font-weight: 600;
        margin: 2px 4px 2px 0;
        letter-spacing: 0.02em;
    }
    .pill-gray   { background: rgba(255,255,255,0.08); color: #cfd2d6; }
    .pill-purple { background: rgba(127,119,221,0.20); color: #b8b2f2; }
    .pill-green  { background: rgba(29,158,117,0.20);  color: #7fe0bd; }
    .pill-red    { background: rgba(226,75,74,0.20);   color: #f4a3a2; }

    .flow-step {
        text-align: center;
        font-size: 11px;
        color: #7a7d84;
        font-weight: 600;
        letter-spacing: 0.03em;
        text-transform: uppercase;
    }

    .quote-box {
        background: #1f2228;
        border-left: 3px solid #7f77dd;
        padding: 10px 14px;
        border-radius: 6px;
        font-size: 14px;
        color: #d7d9dc;
        margin-top: 6px;
    }

    .brand-row {
        display: flex;
        align-items: center;
        gap: 10px;
        margin-bottom: 4px;
    }
    .brand-icon {
        width: 34px; height: 34px; border-radius: 9px;
        background: rgba(127,119,221,0.18);
        display: flex; align-items: center; justify-content: center;
        font-size: 17px;
    }
</style>
""", unsafe_allow_html=True)

# ---- Header ----
st.markdown("""
<div class="brand-row">
    <div class="brand-icon">⚡</div>
    <div>
        <p style="font-weight:600; font-size:17px; margin:0;">Resolution agent</p>
        <p style="font-size:12px; color:#8a8d93; margin:0;">Support &amp; vendor negotiation · online retail</p>
    </div>
</div>
""", unsafe_allow_html=True)

# Static pipeline legend
cols = st.columns(5)
for col, step in zip(cols, ["Observe", "Decide", "Act", "Evaluate", "Adapt"]):
    col.markdown(f"<div class='flow-step'>{step}</div>", unsafe_allow_html=True)

st.divider()

# ---------------------------------------------------------------------------
# Input section
# ---------------------------------------------------------------------------
DATA_DIR = Path(__file__).parent.parent / "data"
with open(DATA_DIR / "tickets_sample.json") as f:
    sample_tickets = json.load(f)

tab_sample, tab_custom = st.tabs(["Sample ticket", "Write your own"])

request_type = None
text = None
request_id = None

with tab_sample:
    ticket_labels = [f"{t['request_id']} · {t['request_type']} — {t['text'][:55]}..." for t in sample_tickets]
    selected_label = st.selectbox("Choose a sample ticket", ticket_labels, label_visibility="collapsed")
    selected_ticket = sample_tickets[ticket_labels.index(selected_label)]

    with st.container(border=True):
        badge_class = "pill-purple" if selected_ticket["request_type"] == "vendor" else "pill-gray"
        st.markdown(
            f"<span class='pill {badge_class}'>{selected_ticket['request_type'].upper()}</span>",
            unsafe_allow_html=True,
        )
        st.write(selected_ticket["text"])

    if st.button("Process this ticket", type="primary", key="process_sample"):
        request_type = selected_ticket["request_type"]
        text = selected_ticket["text"]
        request_id = selected_ticket["request_id"]

with tab_custom:
    custom_type = st.radio("Request type", ["support", "vendor"], horizontal=True)
    custom_text = st.text_area("Request text", placeholder="Type the incoming request here...", height=100)
    if st.button("Process this request", type="primary", key="process_custom"):
        if not custom_text.strip():
            st.warning("Please enter some request text first.")
        else:
            request_type = custom_type
            text = custom_text
            request_id = "manual-request"

# ---------------------------------------------------------------------------
# Pipeline execution
# ---------------------------------------------------------------------------
if request_type and text:
    st.divider()

    with st.status("Running the agent pipeline...", expanded=True) as status:
        st.write("Step 1 — Decision agent classifying request...")
        classification = classify_request(text, request_type)

        st.write("Step 2 — Executing tool...")
        tool_result = run_tool(classification, text, request_type)

        st.write("Step 3 — Evaluating outcome...")
        evaluation = evaluate_outcome(tool_result, request_type)

        status.update(label="Pipeline complete", state="complete", expanded=False)

    # ---- Decision card ----
    with st.container(border=True):
        st.markdown("**Decision agent**")
        badge_class = "pill-purple" if classification["complexity"] == "complex" else "pill-gray"
        st.markdown(
            f"<span class='pill {badge_class}'>{classification['complexity'].upper()}</span>",
            unsafe_allow_html=True,
        )
        st.caption(classification["reason"])

    # ---- Tool result card ----
    with st.container(border=True):
        st.markdown("**Tool execution**")
        if request_type == "support":
            if tool_result["matched"]:
                st.markdown(
                    f"<span class='pill pill-green'>KB MATCH: {tool_result['matched_entry']['topic'].upper()}</span>",
                    unsafe_allow_html=True,
                )
                st.markdown(f"<div class='quote-box'>{tool_result['answer']}</div>", unsafe_allow_html=True)
            else:
                st.markdown("<span class='pill pill-red'>NO KB MATCH</span>", unsafe_allow_html=True)
        else:  # vendor
            if tool_result["quote_found"]:
                quote = tool_result["quote"]
                st.write(f"**{quote['vendor_name']}** — {quote['item']}")
                m1, m2 = st.columns(2)
                m1.metric("Quoted price", f"₹{quote['quoted_price']:,}")
                m2.metric(
                    "Our target price",
                    f"₹{quote['threshold_price']:,}",
                    delta=f"₹{quote['quoted_price'] - quote['threshold_price']:,} over target",
                    delta_color="inverse",
                )
                if tool_result.get("counter_offer_text"):
                    st.markdown(f"<div class='quote-box'>{tool_result['counter_offer_text']}</div>", unsafe_allow_html=True)
            else:
                st.markdown("<span class='pill pill-red'>NO VENDOR QUOTE FOUND</span>", unsafe_allow_html=True)

    # ---- Evaluation + Outcome ----
    if evaluation["accepted"]:
        st.success(f"**Auto-resolved** — accepted (`{evaluation['reason']}`). No human needed.")
    else:
        escalation_entry = escalate(request_id, text, tool_result, evaluation)
        st.error(f"**Escalated to human** — reason: `{evaluation['reason']}`")
        with st.expander("View full escalation log entry"):
            st.json(escalation_entry)

st.divider()
st.caption("Every escalation is saved to `logs/decisions.log` with full reasoning, for auditability.")