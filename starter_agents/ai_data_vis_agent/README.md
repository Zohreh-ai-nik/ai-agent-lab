# 📊 AI Data Visualization Agent

Upload any dataset and ask questions in plain English — the AI agent analyzes your data and generates visualizations instantly.

---

## What it does

- Upload a CSV file
- Ask a question like "show me sales by region" or "what is the distribution of age?"
- The AI writes and runs Python code automatically
- You get a chart + statistics + explanation

---

## Stack

- **Together AI** — LLM provider (Llama, DeepSeek, Qwen)
- **E2B** — secure sandbox to execute generated code
- **Streamlit** — UI

---

## API Keys needed

| Service | Free? | Link |
|---------|-------|------|
| Together AI | ✅ Free | https://api.together.ai |
| E2B | ✅ Free | https://e2b.dev |

---

## Quick Start

```bash
# 1. Go to project folder
cd starter_agents/ai_data_viz_agent

# 2. Copy env template and fill in your keys
cp .env.example .env

# 3. Install dependencies (venv must be active at repo root)
pip install -r requirements.txt

# 4. Run the app
streamlit run ai_data_viz_agent.py
```

---

## .env file

```env
TOGETHER_API_KEY=your_together_ai_key_here
E2B_API_KEY=your_e2b_key_here
```

---

## How to use

1. Open the app at `http://localhost:8501`
2. Enter your API keys in the sidebar
3. Choose your preferred LLM model
4. Upload a CSV file
5. Type your question in plain English
6. Click **Analyze** and get your chart