"""
Streamlit UI: full dashboard layout (sidebar + header + content + footer),
dark tech-startup theme. The dark palette itself comes from
.streamlit/config.toml; this file adds sidebar navigation, session stats,
and card styling on top of it.
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
# Page setup + styling
# ---------------------------------------------------------------------------
st.set_page_config(page_title="Resolution Agent", page_icon="⚡", layout="wide")

st.markdown("""
<style>
    .pill {
        display: inline-block; padding: 4px 14px; border-radius: 999px;
        font-size: 12px; font-weight: 600; margin: 2px 4px 2px 0; letter-spacing: 0.02em;
    }
    .pill-gray   { background: rgba(255,255,255,0.08); color: #cfd2d6; }
    .pill-purple { background: rgba(127,119,221,0.20); color: #b8b2f2; }
    .pill-green  { background: rgba(29,158,117,0.20);  color: #7fe0bd; }
    .pill-red    { background: rgba(226,75,74,0.20);   color: #f4a3a2; }

    .quote-box {
        background: #1f2228; border-left: 3px solid #7f77dd; padding: 10px 14px;
        border-radius: 6px; font-size: 14px; color: #d7d9dc; margin-top: 6px;
    }

    .brand-row { display: flex; align-items: center; gap: 10px; margin-bottom: 8px; }
    .brand-icon {
        width: 30px; height: 30px; border-radius: 8px; background: rgba(127,119,221,0.18);
        display: flex; align-items: center; justify-content: center; font-size: 15px;
    }

    .stat-card {
        background: #1a1c21; border: 0.5px solid #24262c; border-radius: 8px;
        padding: 8px 10px; margin-bottom: 8px;
    }
    .stat-label { font-size: 10px; color: #8a8d93; margin: 0; }
    .stat-value { font-size: 18px; font-weight: 600; margin: 0; }

    .live-badge {
        font-size: 11px; padding: 4px 10px; border-radius: 999px;
        background: rgba(29,158,117,0.2); color: #7fe0bd; font-weight: 500;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Session state: running stats for the sidebar
# ---------------------------------------------------------------------------
if "processed" not in st.session_state:
    st.session_state.processed = 0
    st.session_state.auto_resolved = 0
    st.session_state.escalated = 0

# ---------------------------------------------------------------------------
# Sidebar: branding, stats, and request input
# ---------------------------------------------------------------------------
DATA_DIR = Path(__file__).parent.parent / "data"
with open(DATA_DIR / "tickets_sample.json") as f:
    sample_tickets = json.load(f)

request_type = None
text = None
request_id = None

with st.sidebar:
    st.markdown("""
    <div class="brand-row">
        <div class="brand-icon">⚡</div>
        <div>
            <p style="font-weight:600; font-size:15px; margin:0;">Resolution Agent</p>
            <p style="font-size:11px; color:#8a8d93; margin:0;">Online retail business</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<p style='font-size:10px; color:#63666d; text-transform:uppercase; letter-spacing:0.05em; margin:14px 0 6px;'>Session stats</p>", unsafe_allow_html=True)
    st.markdown(f"""
    <div class="stat-card"><p class="stat-label">Processed</p><p class="stat-value" style="color:#eaeaea;">{st.session_state.processed}</p></div>
    <div class="stat-card"><p class="stat-label">Auto-resolved</p><p class="stat-value" style="color:#7fe0bd;">{st.session_state.auto_resolved}</p></div>
    <div class="stat-card"><p class="stat-label">Escalated</p><p class="stat-value" style="color:#f4a3a2;">{st.session_state.escalated}</p></div>
    """, unsafe_allow_html=True)

    st.markdown("<p style='font-size:10px; color:#63666d; text-transform:uppercase; letter-spacing:0.05em; margin:16px 0 6px;'>New request</p>", unsafe_allow_html=True)

    tab_sample, tab_custom = st.tabs(["Sample", "Custom"])

    with tab_sample:
        ticket_labels = [f"{t['request_id']} · {t['request_type']}" for t in sample_tickets]
        selected_label = st.selectbox("Ticket", ticket_labels, label_visibility="collapsed")
        selected_ticket = sample_tickets[ticket_labels.index(selected_label)]
        st.caption(selected_ticket["text"][:90] + "...")
        if st.button("Process this ticket", type="primary", key="process_sample", use_container_width=True):
            request_type = selected_ticket["request_type"]
            text = selected_ticket["text"]
            request_id = selected_ticket["request_id"]

    with tab_custom:
        custom_type = st.radio("Type", ["support", "vendor"], horizontal=True, label_visibility="collapsed")
        custom_text = st.text_area("Request text", placeholder="Type the request...", height=90, label_visibility="collapsed")
        if st.button("Process this request", type="primary", key="process_custom", use_container_width=True):
            if not custom_text.strip():
                st.warning("Please enter request text first.")
            else:
                request_type = custom_type
                text = custom_text
                request_id = "manual-request"

# ---------------------------------------------------------------------------
# Hero header — command-center style, using real session data only
# ---------------------------------------------------------------------------
resolution_rate = (
    round(100 * st.session_state.auto_resolved / st.session_state.processed)
    if st.session_state.processed > 0 else None
)

st.markdown("""
<p style='font-size:22px; font-weight:600; margin:0;'>AI operations overview</p>
<p style='font-size:13px; color:#8a8d93; margin:2px 0 16px;'>Resolution agent is actively monitoring incoming requests.</p>
""", unsafe_allow_html=True)

m1, m2, m3, m4 = st.columns(4)
m1.metric("Processed", st.session_state.processed)
m2.metric("Auto-resolved", st.session_state.auto_resolved)
m3.metric("Escalated", st.session_state.escalated)
m4.metric("Resolution rate", f"{resolution_rate}%" if resolution_rate is not None else "—")

st.markdown("""
<div style="margin-top:10px; margin-bottom:6px; display:flex; align-items:center; justify-content:space-between;">
    <div>
        <span style="font-size:15px; font-weight:600;">Live pipeline</span>
        <span style="font-size:12px; color:#8a8d93; margin-left:8px;">Observe → Decide → Act → Evaluate → Adapt</span>
    </div>
    <span class="live-badge">● Live</span>
</div>
""", unsafe_allow_html=True)

st.divider()

# ---------------------------------------------------------------------------
# Activity feed — reads real entries from logs/decisions.log (read-only,
# does not touch the pipeline logic)
# ---------------------------------------------------------------------------
LOG_PATH = Path(__file__).parent.parent / "logs" / "decisions.log"
if LOG_PATH.exists() and LOG_PATH.stat().st_size > 0:
    with open(LOG_PATH) as f:
        log_lines = f.readlines()
    if log_lines:
        with st.expander(f"Activity feed — {len(log_lines)} escalation(s) logged", expanded=False):
            for line in reversed(log_lines[-8:]):
                try:
                    entry = json.loads(line)
                    ts = entry.get("timestamp", "")[11:19]  # just the time part
                    st.markdown(
                        f"<div class='quote-box'><b>{ts}</b> — Ticket {entry.get('request_id', '?')} escalated "
                        f"<span style='color:#8a8d93;'>· reason: {entry.get('reason', 'unknown')}</span></div>",
                        unsafe_allow_html=True,
                    )
                except json.JSONDecodeError:
                    continue


# ---------------------------------------------------------------------------
# Main content: pipeline execution
# ---------------------------------------------------------------------------
if request_type and text:
    with st.status("Running the agent pipeline...", expanded=True) as status:
        st.write("Step 1 — Decision agent classifying request...")
        classification = classify_request(text, request_type)

        st.write("Step 2 — Executing tool...")
        tool_result = run_tool(classification, text, request_type)

        st.write("Step 3 — Evaluating outcome...")
        evaluation = evaluate_outcome(tool_result, request_type)

        status.update(label="Pipeline complete", state="complete", expanded=False)

    # Update session stats
    st.session_state.processed += 1
    if evaluation["accepted"]:
        st.session_state.auto_resolved += 1
    else:
        st.session_state.escalated += 1

    col_a, col_b = st.columns(2)

    with col_a:
        with st.container(border=True):
            st.markdown("**Decision agent**")
            badge_class = "pill-purple" if classification["complexity"] == "complex" else "pill-gray"
            st.markdown(f"<span class='pill {badge_class}'>{classification['complexity'].upper()}</span>", unsafe_allow_html=True)
            st.caption(classification["reason"])

    with col_b:
        with st.container(border=True):
            st.markdown("**Tool execution**")
            if request_type == "support":
                if tool_result["matched"]:
                    st.markdown(f"<span class='pill pill-green'>KB MATCH: {tool_result['matched_entry']['topic'].upper()}</span>", unsafe_allow_html=True)
                else:
                    st.markdown("<span class='pill pill-red'>NO KB MATCH</span>", unsafe_allow_html=True)
            else:
                if tool_result["quote_found"]:
                    st.markdown(f"<span class='pill pill-purple'>{tool_result['quote']['vendor_name'].upper()}</span>", unsafe_allow_html=True)
                else:
                    st.markdown("<span class='pill pill-red'>NO QUOTE FOUND</span>", unsafe_allow_html=True)

    # Full-width detail card
    with st.container(border=True):
        if request_type == "support" and tool_result["matched"]:
            st.markdown(f"<div class='quote-box'>{tool_result['answer']}</div>", unsafe_allow_html=True)
            action_result = tool_result.get("action_result")
            if action_result:
                action_badge = "pill-red" if action_result["status"] == "blocked" else "pill-green"
                st.markdown(
                    f"<div style='margin-top:10px;'><span class='pill {action_badge}'>ACTION: {action_result['action'].upper()} — {action_result['status'].upper()}</span></div>",
                    unsafe_allow_html=True,
                )
                if action_result["status"] == "blocked":
                    st.caption(f"Blocked reason: {action_result['block_reason']}")
        elif request_type == "vendor" and tool_result["quote_found"]:
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

    # Outcome banner
    if evaluation["accepted"]:
        st.success(f"**Auto-resolved** — accepted (`{evaluation['reason']}`). No human needed.")
    else:
        escalation_entry = escalate(request_id, text, tool_result, evaluation)
        st.error(f"**Escalated to human** — reason: `{evaluation['reason']}`")
        with st.expander("View full escalation log entry"):
            st.json(escalation_entry)
else:
    st.info("Pick a sample ticket or write your own request in the sidebar, then click Process.")

# ---------------------------------------------------------------------------
# Footer
# ---------------------------------------------------------------------------
st.divider()
st.caption("Decision log saved to `logs/decisions.log` · Agentic AI Hackathon, Tech Zephyr 4.0, IIT Bhubaneswar")