# agents_setup.py
# ─────────────────────────────────────────────────────────────
# Purpose: Define all three agents in the multi-agent pipeline.
#
# Agent roles:
#   research_agent – searches the web and summarises findings
#   editor_agent   – writes the final structured markdown report
#   triage_agent   – coordinator: plans the research, then hands
#                    off to research_agent and editor_agent
#
# Key SDK concepts used here:
#
#   Agent(name, instructions, model, tools, output_type)
#     Creates an LLM-backed agent. `output_type` forces the model
#     to return JSON matching a Pydantic schema.
#
#   WebSearchTool()
#     Built-in tool from the `agents` SDK. Gives an agent the
#     ability to run live web searches during its turn.
#
#   handoff(agent)
#     Tells the triage_agent it is allowed to hand control to
#     another agent. The LLM decides when to hand off based on
#     its instructions and the conversation so far.
#
#   handoff_description
#     A short string that tells the triage_agent what the target
#     agent does — helps the LLM decide who to hand off to.
# ─────────────────────────────────────────────────────────────

from agents import Agent, WebSearchTool, handoff

from models import ResearchPlan, ResearchReport
from tools import save_important_fact


# ── Agent 1: Research Agent ───────────────────────────────────
# Does the actual information gathering. Given a search query,
# it calls WebSearchTool and writes a concise summary.
# It also calls save_important_fact for key findings.

research_agent = Agent(
    name="Research Agent",
    instructions=(
        "You are a research assistant. Given a search term, search the web "
        "and produce a concise summary of the results. "
        "The summary must be 2-3 paragraphs and under 300 words. "
        "Capture the main points. Write succinctly — no need for complete "
        "sentences or perfect grammar. This will be consumed by someone "
        "synthesizing a report, so capture the essence and ignore fluff. "
        "Do not add commentary beyond the summary itself."
    ),
    model="gpt-4o-mini",
    tools=[
        WebSearchTool(),
        save_important_fact,   # custom tool defined in tools.py
    ],
)


# ── Agent 2: Editor Agent ─────────────────────────────────────
# Receives the full research history and writes the final report.
# output_type=ResearchReport forces it to return structured JSON.

editor_agent = Agent(
    name="Editor Agent",
    handoff_description="A senior researcher who writes comprehensive research reports",
    instructions=(
        "You are a senior researcher tasked with writing a cohesive report. "
        "You will receive the original query and the research done by the "
        "Research Agent.\n"
        "First create a detailed outline, then write the full report in "
        "markdown format. Aim for 5-10 pages of content, at least 1000 words."
    ),
    model="gpt-4o-mini",
    output_type=ResearchReport,   # enforces structured JSON output
)


# ── Agent 3: Triage Agent ─────────────────────────────────────
# Entry point of the pipeline. It:
#   1. Creates a ResearchPlan (output_type enforces structure)
#   2. Hands off to research_agent for information gathering
#   3. Hands off to editor_agent for report writing

triage_agent = Agent(
    name="Triage Agent",
    instructions=(
        "You are the coordinator of this research operation. Your job is to:\n"
        "1. Understand the user's research topic.\n"
        "2. Create a research plan with:\n"
        "   - topic: A clear statement of the research topic\n"
        "   - search_queries: 3-5 specific search queries\n"
        "   - focus_areas: 3-5 key aspects to investigate\n"
        "3. Hand off to the Research Agent to collect information.\n"
        "4. After research is complete, hand off to the Editor Agent "
        "to write the comprehensive report.\n"
        "Return your plan in the expected structured format."
    ),
    handoffs=[
        handoff(research_agent),
        handoff(editor_agent),
    ],
    model="gpt-4o-mini",
    output_type=ResearchPlan,
)