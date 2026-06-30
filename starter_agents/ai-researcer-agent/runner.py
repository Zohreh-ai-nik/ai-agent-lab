# runner.py
# ─────────────────────────────────────────────────────────────
# Purpose: Contain all async orchestration logic, completely
#          separated from the Streamlit UI.
#
# Why separate this from app.py?
#   app.py should only handle display (what the user sees).
#   runner.py handles the "what happens when research runs"
#   logic. This makes both files easier to read and test.
#
# Key SDK concepts:
#
#   Runner.run(agent, input)
#     Runs an agent with a given input string. Returns a result
#     object. `result.final_output` holds the agent's last
#     structured or text output.
#
#   result.to_input_list()
#     Converts the full conversation history from one run into
#     a format that can be passed as input to the next run.
#     This is how the Editor Agent receives everything the
#     Research Agent found — the full chain of messages is
#     passed forward, not just a summary.
#
#   trace(name, group_id)
#     Wraps a block of agent runs into a named trace for
#     debugging in the OpenAI dashboard. group_id groups all
#     runs from one user session together.
# ─────────────────────────────────────────────────────────────

import asyncio
import streamlit as st
from agents import Runner, trace

from agents_setup import triage_agent, editor_agent


async def run_research(topic: str, conversation_id: str) -> dict:
    """
    Orchestrate the full multi-agent research pipeline.

    Flow:
      1. Triage Agent  → creates ResearchPlan
      2. Research Agent → called by triage internally via handoff
      3. Editor Agent  → receives full history, writes ResearchReport

    Args:
        topic:           The user's research topic string.
        conversation_id: UUID string used to group traces.

    Returns:
        A dict with keys:
          "plan"   → ResearchPlan object (or fallback dict)
          "report" → ResearchReport object (or raw string)
          "error"  → error message string, or None
    """
    result = {"plan": None, "report": None, "error": None}

    # Reset fact collection for this new run
    st.session_state.collected_facts = []

    with trace("News Research", group_id=conversation_id):

        # ── Phase 1: Triage Agent creates the research plan ──
        triage_result = await Runner.run(
            triage_agent,
            f"Research this topic thoroughly: {topic}. "
            "This research will be used to create a comprehensive research report.",
        )

        # Extract the ResearchPlan if properly structured
        if hasattr(triage_result.final_output, "topic"):
            result["plan"] = triage_result.final_output
        else:
            # Fallback: triage didn't return structured output
            result["plan"] = {
                "topic": topic,
                "search_queries": [f"Researching {topic}"],
                "focus_areas": [f"General information about {topic}"],
            }

        # ── Phase 2: Editor Agent writes the report ───────────
        # `to_input_list()` passes the FULL conversation history
        # from the triage+research phase to the editor. The editor
        # sees every search result and fact that was gathered.
        try:
            report_result = await Runner.run(
                editor_agent,
                triage_result.to_input_list(),
            )
            result["report"] = report_result.final_output

        except Exception as e:
            result["error"] = str(e)

            # Attempt to salvage raw text from the triage result
            if hasattr(triage_result, "new_items"):
                messages = [
                    item for item in triage_result.new_items
                    if hasattr(item, "content") and item.content
                ]
                if messages:
                    result["report"] = "\n\n".join(
                        str(m.content) for m in messages
                    )

    return result