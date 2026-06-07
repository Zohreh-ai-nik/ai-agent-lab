from utils import extract_python_code


response_with_code = "Here is the code:\n```python\nprint('hello')\n```\nHope that helps!"
result = extract_python_code(response_with_code)
print(result)  # Output: print('hello')