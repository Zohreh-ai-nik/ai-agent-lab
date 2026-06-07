## llm.py
# PURPOSE: All Together AI / LLM interactions in one place
from typing import Tuple
import anthropic
from utils import extract_python_code
from dotenv import load_dotenv
import os

load_dotenv()  # reads your .env file and loads the keys into os.environ


def build_system_prompt(dataset_path: str) -> str:
    """build the system prompt telling llm where the dataset is and what its job is

    """
    return  f"""You are a Python data scientist and data visualization expert.
You are given a dataset at path '{dataset_path}'.
Analyze the dataset and answer the user's question.
Always write Python code in a ```python ... ``` block.
Always use '{dataset_path}' when reading the CSV file.
Use matplotlib or seaborn for visualizations.
Always call plt.show() at the end of your plot code."""


def ask_llm(
    api_key: str,
    model:str,
    user_message:str,
    dataset_path:str
) -> Tuple[str, str]:
    """
    Sends user message to the LLM.
    Returns a tuple of (full_response_text, extracted_python_code).
    """
    client = anthropic.Anthropic(api_key=api_key)
    response = client.messages.create(
        model=model,
        max_tokens=3000,
        system=build_system_prompt(dataset_path),
        messages=[{"role": "user", "content": user_message}]
    )
    full_response = response.content[0].text
    python_code = extract_python_code(full_response)
    return full_response, python_code
    
    
if __name__ == "__main__":
    
    api_key = os.getenv("ANTHROPIC_API_KEY")
    print("sending the request for anthropic ai")
    
    full_response, python_code = ask_llm(
        api_key=api_key,
        model="claude-sonnet-4-20250514",
        user_message="Write Python code to print the numbers 1 to 5",
        dataset_path="./data.csv"
    )   
    
    print("Full LLM Response:")
    print(full_response)
    print("Extracted Python Code:")
    print(python_code)
