# app.py
# ─────────────────────────────────────────────────────────────
# Purpose: Streamlit UI — display only. No agent logic here.
#
# Structure:
#   - Page config and API key check
#   - Sidebar: topic input + example topics
#   - Tab 1 "Research Process": live progress during the run
#   - Tab 2 "Report": full structured report with download button
#
# Why asyncio.run()?
#   Streamlit runs synchronously. Our runner.py uses async/await
#   (required by the OpenAI Agents SDK). asyncio.run() bridges
#   the two: it starts an event loop, runs the coroutine to
#   completion, and returns the result back to the sync world.
# ─────────────────────────────────────────────────────────────

import os
import uuid
import asyncio
import streamlit as st
from dotenv import load_dotenv

from runner import run_research

load_dotenv()

# ── Page setup ────────────────────────────────────────────────
st.set_page_config(
    page_title="AI Researcher Agent",
    page_icon="📰",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── API key guard ─────────────────────────────────────────────
if not os.environ.get("OPENAI_API_KEY"):
    st.error("Please set your OPENAI_API_KEY environment variable")
    st.stop()

# ── Header ────────────────────────────────────────────────────
st.title("📰 AI Researcher Agent")
st.subheader("Powered by OpenAI Agents SDK")
st.markdown(
    "A multi-agent system that researches any topic and generates "
    "a comprehensive markdown report — automatically."
)

# ── Session state initialisation ──────────────────────────────
# These keys persist across Streamlit reruns within one session.
if "conversation_id" not in st.session_state:
    st.session_state.conversation_id = uuid.uuid4().hex[:16]
if "collected_facts" not in st.session_state:
    st.session_state.collected_facts = []
if "research_done" not in st.session_state:
    st.session_state.research_done = False
if "result" not in st.session_state:
    st.session_state.result = None

# ── Sidebar ───────────────────────────────────────────────────
with st.sidebar:
    st.header("Research Topic")
    user_topic = st.text_input("Enter a topic to research:")

    start_button = st.button(
        "Start Research", type="primary", disabled=not user_topic
    )

    st.divider()
    st.subheader("Example Topics")

    example_topics = [
        "Best cruise lines in the USA for first-time travelers",
        "Best affordable espresso machines for someone upgrading from a French press",
        "Off-the-beaten-path destinations in India for solo travelers",
    ]

    for topic in example_topics:
        if st.button(topic, key=topic):
            user_topic = topic
            start_button = True

# ── Tabs ──────────────────────────────────────────────────────
tab1, tab2 = st.tabs(["Research Process", "Report"])

# ── Run research ──────────────────────────────────────────────
if start_button and user_topic:
    st.session_state.research_done = False
    st.session_state.result = None

    with tab1:
        st.write("🔍 **Triage Agent**: Planning research approach...")
        progress_placeholder = st.empty()
        fact_placeholder = st.empty()

    with st.spinner(f"Researching: {user_topic}"):
        try:
            result = asyncio.run(
                run_research(user_topic, st.session_state.conversation_id)
            )
            st.session_state.result = result
            st.session_state.research_done = True

        except Exception as e:
            st.error(f"An error occurred: {e}")
            st.session_state.research_done = True

    # Show plan and facts after run completes
    with tab1:
        if st.session_state.result:
            plan = st.session_state.result.get("plan")
            if plan:
                st.write("📋 **Research Plan**:")
                if hasattr(plan, "model_dump"):
                    st.json(plan.model_dump())
                else:
                    st.json(plan)

            if st.session_state.collected_facts:
                st.write("📚 **Collected Facts**:")
                for fact in st.session_state.collected_facts:
                    st.info(
                        f"**Fact**: {fact['fact']}\n\n"
                        f"**Source**: {fact['source']}"
                    )

            error = st.session_state.result.get("error")
            if error:
                st.warning(f"⚠️ Issue during report generation: {error}")
            else:
                st.success("✅ Research complete! See the Report tab.")

# ── Report tab ────────────────────────────────────────────────
with tab2:
    if st.session_state.research_done and st.session_state.result:
        report = st.session_state.result.get("report")

        if report is None:
            st.warning("No report was generated.")

        elif hasattr(report, "title"):
            # Properly structured ResearchReport object
            st.title(report.title)

            if report.outline:
                with st.expander("Report Outline", expanded=True):
                    for i, section in enumerate(report.outline, 1):
                        st.markdown(f"{i}. {section}")

            if report.word_count:
                st.info(f"Word count: {report.word_count}")

            st.markdown(report.report)

            if report.sources:
                with st.expander("Sources"):
                    for i, source in enumerate(report.sources, 1):
                        st.markdown(f"{i}. {source}")

            st.download_button(
                label="Download Report",
                data=report.report,
                file_name=f"{report.title.replace(' ', '_')}.md",
                mime="text/markdown",
            )

        else:
            # Fallback: raw string response
            st.markdown(str(report))
            st.download_button(
                label="Download Report",
                data=str(report),
                file_name="research_report.md",
                mime="text/markdown",
            )
    else:
        st.info("Run a research query to see the report here.")