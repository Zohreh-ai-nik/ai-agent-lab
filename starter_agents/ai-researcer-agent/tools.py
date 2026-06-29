# tools.py
# ─────────────────────────────────────────────────────────────
# Purpose: Define custom tools that agents can call during a run.
#
# How @function_tool works:
#   The `@function_tool` decorator from `agents` converts a plain
#   Python function into a tool the SDK can pass to an LLM.
#   The LLM sees the function name, its docstring, and the type-
#   annotated parameters — it decides when to call it on its own.
#
# Why store facts in st.session_state?
#   Streamlit reruns the whole script on each interaction. Using
#   st.session_state keeps data alive across reruns so we can
#   display collected facts in real time in the UI.
# ─────────────────────────────────────────────────────────────

import streamlit as st
from datetime import datetime
from agents import function_tool


@function_tool
def save_important_fact(fact: str, source: str = None) -> str:
    """
    Save an important fact discovered during research.

    The Research Agent calls this whenever it finds something
    worth highlighting. Facts are stored in Streamlit session
    state so the UI can display them live as research runs.

    Args:
        fact:   The important fact to save.
        source: Optional URL or publication name as the source.

    Returns:
        A confirmation string (the SDK passes this back to the LLM).
    """
    # Initialize storage on first call
    if "collected_facts" not in st.session_state:
        st.session_state.collected_facts = []

    st.session_state.collected_facts.append({
        "fact": fact,
        "source": source or "Not specified",
        "timestamp": datetime.now().strftime("%H:%M:%S"),
    })

    return f"Fact saved: {fact}"