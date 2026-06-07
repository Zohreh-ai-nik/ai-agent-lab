#helper function used across the app
# utils.py
# PURPOSE: Helper functions used across the app
import re

# This pattern finds python code blocks in LLM responses
# Example: ```python\nprint('hello')\n``` → extracts print('hello')
pattern = re.compile(r"```python\n(.*?)\n```", re.DOTALL)

def extract_python_code(llm_response: str) -> str:
    """
    Extracts Python code from LLM markdown response.
    Returns empty string if no code block found.
    """
    match = pattern.search(llm_response)
    if match:
        return match.group(1)
    return ""