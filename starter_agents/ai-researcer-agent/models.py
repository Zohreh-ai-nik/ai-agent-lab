# models.py
# ─────────────────────────────────────────────────────────────
# Purpose: Define the structured data models used across the
#          multi-agent pipeline.
#
# Why Pydantic?
#   The OpenAI Agents SDK supports `output_type=SomeModel` on
#   an Agent. When set, the SDK forces the LLM to return valid
#   JSON that matches that schema — no manual parsing needed.
#
# Models:
#   ResearchPlan   → output of the Triage Agent
#   ResearchReport → output of the Editor Agent
# ─────────────────────────────────────────────────────────────

from pydantic import BaseModel


class ResearchPlan(BaseModel):
    """
    Structured plan created by the Triage Agent before any
    research begins.

    Fields:
      topic          – one-sentence statement of what to research
      search_queries – 3-5 specific queries for the Research Agent
      focus_areas    – 3-5 key angles the report should cover
    """
    topic: str
    search_queries: list[str]
    focus_areas: list[str]


class ResearchReport(BaseModel):
    """
    Final deliverable created by the Editor Agent.

    Fields:
      title      – title of the report
      outline    – ordered list of section headings
      report     – full markdown body (target: 1000+ words)
      sources    – URLs or citations collected during research
      word_count – approximate word count of the report body
    """
    title: str
    outline: list[str]
    report: str
    sources: list[str]
    word_count: int