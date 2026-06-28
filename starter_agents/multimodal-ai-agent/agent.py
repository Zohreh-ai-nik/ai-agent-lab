from agno.agent import Agent
from agno.model.Anthropic import Claude
from agno.model.OpenAI import ChatGPT

def create_agent(api_key: str) -> Agent:
    
    agent = Agent(
        model=Claude(id="claude-haiku-4-5", api_key=api_key),
        markdown=True
    )
    return agent


