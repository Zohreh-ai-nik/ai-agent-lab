# agent.py
# PURPOSE: Agno agent setup — brain of the app
import os
from typing import Optional
from dotenv import load_dotenv
from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.tools.e2b import E2BTools
from agno.tools.firecrawl import FirecrawlTools

load_dotenv()


def get_agent(
    openai_key: str,
    firecrawl_key: str,
    e2b_key: str
) -> Optional[Agent]:
    """
    Creates and returns the insurance advisor agent.
    Returns None if any key is missing.
    """
    if not (openai_key and firecrawl_key and e2b_key):
        print("❌ Missing API keys")
        return None

    # Set environment variables for tools
    os.environ["OPENAI_API_KEY"]    = openai_key
    os.environ["FIRECRAWL_API_KEY"] = firecrawl_key
    os.environ["E2B_API_KEY"]       = e2b_key

    return Agent(
        name="Life Insurance Advisor",
        model=OpenAIChat(
            id="gpt-4o-mini",
            api_key=openai_key,
        ),
        tools=[
            E2BTools(timeout=180),
            FirecrawlTools(
                api_key=firecrawl_key,
                enable_search=True,
                enable_crawl=True,
                enable_scrape=False,
                search_params={"limit": 5, "lang": "en"},
            ),
        ],
        instructions=[
            "You provide conservative life insurance guidance.",
            "Your workflow is strictly:",
            "1. Use E2B to compute coverage recommendation from client JSON.",
            "   - Use default real discount rate of 2%.",
            "   - Formula: discounted_income = annual_income * ((1-(1+r)**(-years))/r)",
            "   - Recommended = max(0, discounted_income + total_debt - savings - existing_cover)",
            "2. Use Firecrawl to search for current term life insurance products.",
            "3. Respond ONLY with JSON with these keys:",
            "   coverage_amount, coverage_currency, breakdown,",
            "   assumptions, recommendations, research_notes, timestamp",
            "Do not include markdown or commentary — pure JSON only.",
        ],
        markdown=False,
    )


# ── Run directly to test agent creation ──────────────────
if __name__ == "__main__":
    openai_key    = os.getenv("OPENAI_API_KEY")
    firecrawl_key = os.getenv("FIRECRAWL_API_KEY")
    e2b_key       = os.getenv("E2B_API_KEY")

    print("⏳ Creating agent...")
    agent = get_agent(openai_key, firecrawl_key, e2b_key)

    if agent:
        print("✅ Agent created successfully!")
        print(f"✅ Agent name: {agent.name}")
        print(f"✅ Tools: {[t.__class__.__name__ for t in agent.tools]}")
    else:
        print("❌ Agent creation failed — check your API keys")