# 🤖 LLM Providers — Swap Guide

> How to switch between Together AI, Claude, and OpenAI in `llm.py`.
> Only `llm.py` and `.env` change — nothing else.

---

## 📦 The 3 Providers at a Glance

| | Together AI | Claude (Anthropic) | OpenAI |
|--|-------------|--------|--------|
| Import | `from together import Together` | `import anthropic` | `from openai import OpenAI` |
| Client | `Together(api_key=)` | `anthropic.Anthropic(api_key=)` | `OpenAI(api_key=)` |
| API call | `client.chat.completions.create()` | `client.messages.create()` | `client.chat.completions.create()` |
| System prompt | inside `messages[]` | separate `system=` parameter | inside `messages[]` |
| Get response | `response.choices[0].message.content` | `response.content[0].text` | `response.choices[0].message.content` |
| `.env` key | `TOGETHER_API_KEY` | `ANTHROPIC_API_KEY` | `OPENAI_API_KEY` |
| Free tier | ✅ $1 credit | ❌ Pay from start | ❌ Pay from start |

---

## 1️⃣ Together AI

### .env
```env
TOGETHER_API_KEY=your_key_here
E2B_API_KEY=your_key_here
```

### requirements.txt
```txt
together==1.3.3
streamlit==1.32.0
e2b-code-interpreter==0.0.10
pandas==2.2.0
python-dotenv==1.0.0
pillow==10.2.0
```

### llm.py
```python
# llm.py
from typing import Tuple
from together import Together
from utils import extract_python_code
from dotenv import load_dotenv
import os

load_dotenv()


def build_system_prompt(dataset_path: str) -> str:
    return f"""You are a Python data scientist and data visualization expert.
You are given a dataset at path '{dataset_path}'.
Analyze the dataset and answer the user's question.
Always write Python code in a ```python ... ``` block.
Always use '{dataset_path}' when reading the CSV file.
Use matplotlib or seaborn for visualizations.
Always call plt.show() at the end of your plot code."""


def ask_llm(
    api_key: str,
    model: str,
    user_message: str,
    dataset_path: str
) -> Tuple[str, str]:
    client = Together(api_key=api_key)

    messages = [
        {"role": "system", "content": build_system_prompt(dataset_path)},
        {"role": "user",   "content": user_message}
    ]

    response = client.chat.completions.create(
        model=model,
        messages=messages
    )

    full_response = response.choices[0].message.content
    python_code = extract_python_code(full_response)
    return full_response, python_code


if __name__ == "__main__":
    api_key = os.getenv("TOGETHER_API_KEY")
    print(f"✅ Key loaded: {api_key[:8]}...")
    print("⏳ Sending request to Together AI...")
    full_response, python_code = ask_llm(
        api_key=api_key,
        model="meta-llama/Llama-3.3-70B-Instruct-Turbo",
        user_message="Write Python code to print numbers 1 to 5",
        dataset_path="./data.csv"
    )
    print("\n📨 Full response:")
    print(full_response)
    print("\n🐍 Extracted code:")
    print(python_code)
```

### Available models
```
meta-llama/Llama-3.3-70B-Instruct-Turbo
meta-llama/Meta-Llama-3.1-405B-Instruct-Turbo
deepseek-ai/DeepSeek-V3
Qwen/Qwen2.5-7B-Instruct-Turbo
```

### Get API key
👉 https://api.together.ai

---

## 2️⃣ Claude (Anthropic)

### .env
```env
ANTHROPIC_API_KEY=your_key_here
E2B_API_KEY=your_key_here
```

### requirements.txt
```txt
anthropic==0.40.0
httpx==0.27.0
streamlit==1.32.0
e2b-code-interpreter==0.0.10
pandas==2.2.0
python-dotenv==1.0.0
pillow==10.2.0
```

### llm.py
```python
# llm.py
from typing import Tuple
import anthropic
from utils import extract_python_code
from dotenv import load_dotenv
import os

load_dotenv()


def build_system_prompt(dataset_path: str) -> str:
    return f"""You are a Python data scientist and data visualization expert.
You are given a dataset at path '{dataset_path}'.
Analyze the dataset and answer the user's question.
Always write Python code in a ```python ... ``` block.
Always use '{dataset_path}' when reading the CSV file.
Use matplotlib or seaborn for visualizations.
Always call plt.show() at the end of your plot code."""


def ask_llm(
    api_key: str,
    model: str,
    user_message: str,
    dataset_path: str
) -> Tuple[str, str]:
    client = anthropic.Anthropic(api_key=api_key)

    response = client.messages.create(
        model=model,
        max_tokens=2048,
        system=build_system_prompt(dataset_path),
        messages=[
            {"role": "user", "content": user_message}
        ]
    )

    full_response = response.content[0].text
    python_code = extract_python_code(full_response)
    return full_response, python_code


if __name__ == "__main__":
    api_key = os.getenv("ANTHROPIC_API_KEY")
    print(f"✅ Key loaded: {api_key[:8]}...")
    print("⏳ Sending request to Claude...")
    full_response, python_code = ask_llm(
        api_key=api_key,
        model="claude-sonnet-4-20250514",
        user_message="Write Python code to print numbers 1 to 5",
        dataset_path="./data.csv"
    )
    print("\n📨 Full response:")
    print(full_response)
    print("\n🐍 Extracted code:")
    print(python_code)
```

### Available models
```
claude-sonnet-4-20250514       ← smart, best for complex tasks
claude-haiku-4-5-20251001      ← fast and cheap
```

### Get API key
👉 https://console.anthropic.com

### Fix common error: proxies TypeError
```bash
pip install anthropic --upgrade
pip install httpx --upgrade
```

---

## 3️⃣ OpenAI

### .env
```env
OPENAI_API_KEY=your_key_here
E2B_API_KEY=your_key_here
```

### requirements.txt
```txt
openai==1.14.0
streamlit==1.32.0
e2b-code-interpreter==0.0.10
pandas==2.2.0
python-dotenv==1.0.0
pillow==10.2.0
```

### llm.py
```python
# llm.py
from typing import Tuple
from openai import OpenAI
from utils import extract_python_code
from dotenv import load_dotenv
import os

load_dotenv()


def build_system_prompt(dataset_path: str) -> str:
    return f"""You are a Python data scientist and data visualization expert.
You are given a dataset at path '{dataset_path}'.
Analyze the dataset and answer the user's question.
Always write Python code in a ```python ... ``` block.
Always use '{dataset_path}' when reading the CSV file.
Use matplotlib or seaborn for visualizations.
Always call plt.show() at the end of your plot code."""


def ask_llm(
    api_key: str,
    model: str,
    user_message: str,
    dataset_path: str
) -> Tuple[str, str]:
    client = OpenAI(api_key=api_key)

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": build_system_prompt(dataset_path)},
            {"role": "user",   "content": user_message}
        ]
    )

    full_response = response.choices[0].message.content
    python_code = extract_python_code(full_response)
    return full_response, python_code


if __name__ == "__main__":
    api_key = os.getenv("OPENAI_API_KEY")
    print(f"✅ Key loaded: {api_key[:8]}...")
    print("⏳ Sending request to OpenAI...")
    full_response, python_code = ask_llm(
        api_key=api_key,
        model="gpt-4o",
        user_message="Write Python code to print numbers 1 to 5",
        dataset_path="./data.csv"
    )
    print("\n📨 Full response:")
    print(full_response)
    print("\n🐍 Extracted code:")
    print(python_code)
```

### Available models
```
gpt-4o           ← best quality
gpt-4o-mini      ← fast and cheap
gpt-3.5-turbo    ← legacy, very cheap
```

### Get API key
👉 https://platform.openai.com

---

## ⚡ How to switch provider — 3 steps only

1. Update `.env` with the right key
2. Update `requirements.txt` with the right package
3. Replace `llm.py` with the version above

Nothing else changes. `utils.py`, `sandbox.py`, and `app.py` stay exactly the same.

---

*ai-agent-lab by Zohreh-ai-nik*