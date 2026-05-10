from __future__ import annotations

import os
import sys
import uuid

import pandas as pd
import streamlit as st

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.config import settings
from core.db import SupportDB
from core.orchestrator import AgentOrchestrator
from core.vector_store import KnowledgeBase


st.set_page_config(page_title="Agentic AI Customer Support Chatbot", layout="wide")
st.title("Agentic AI Customer Support Chatbot")
st.caption("Enterprise-style multi-agent support assistant demo")

if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())[:8]

with st.sidebar:
    st.subheader("Configuration")
    provider = st.selectbox(
        "LLM Provider",
        ["openai", "gemini", "ollama"],
        index=["openai", "gemini", "ollama"].index(settings.llm_provider)
        if settings.llm_provider in ["openai", "gemini", "ollama"]
        else 0,
    )
    st.write(f"Session ID: {st.session_state.session_id}")
    st.info(
        "Tip: run scripts/ingest_kb.py once before chatting for best RAG responses."
    )

# Boot core services
db = SupportDB(settings.sqlite_db_path)
kb = KnowledgeBase(settings.vector_db_path)
orchestrator = AgentOrchestrator(db=db, kb=kb, llm_provider=provider)

history = db.get_history(st.session_state.session_id, limit=30)
for msg in history:
    with st.chat_message(msg["role"]):
        st.markdown(msg["message"])

user_query = st.chat_input("Type your support question...")
if user_query:
    with st.chat_message("user"):
        st.markdown(user_query)

    with st.chat_message("assistant"):
        result = orchestrator.handle(st.session_state.session_id, user_query)
        st.markdown(result["response"])
        with st.expander("Agent Trace"):
            st.json(result["trace"])

st.divider()
st.subheader("Operations Dashboard")

tickets = db.list_tickets()
if tickets:
    ticket_df = pd.DataFrame(tickets)
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Open Tickets", int((ticket_df["status"] == "open").sum()))
    with col2:
        high_pri = int((ticket_df["priority"] == "high").sum())
        st.metric("High Priority Tickets", high_pri)

    st.dataframe(ticket_df, use_container_width=True)
else:
    st.write("No tickets created yet.")
