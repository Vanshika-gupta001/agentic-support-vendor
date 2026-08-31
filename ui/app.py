"""
Streamlit UI: chat-style front end for the demo.

TODO (Member 2):
- Text input for a request + dropdown for request_type (support/vendor)
- Call the FastAPI /process endpoint (or import agent functions directly)
- Show the full trail: classification -> tool result -> evaluation -> outcome
- This is what judges will see live, so keep it clean and readable
"""

import streamlit as st

st.set_page_config(page_title="Agentic Resolution Demo", layout="centered")
st.title("Autonomous Vendor & Support Resolution Agent")

request_type = st.selectbox("Request type", ["support", "vendor"])
text = st.text_area("Incoming request")

if st.button("Process"):
    st.info("TODO: wire this up to the FastAPI backend / agent pipeline")
