from agno.agent import Agent
from agno.models.anthropic import Claude

def create_agent(api_key: str) -> Agent:
    
    agent = Agent(
        model=Claude(id="claude-haiku-4-5", api_key=api_key),
        markdown=True
    )
    return agent

if __name__ == "__main__":
    agent = create_agent(api_key="fake-key-just-to-test-structure")
    print("Agent created:", agent.model.id)
