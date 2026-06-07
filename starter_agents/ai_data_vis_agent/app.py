# app.py
# PURPOSE: Streamlit UI only — no business logic here
import streamlit as st
import pandas as pd
from llm import ask_llm
from sandbox import create_sandbox, upload_dataset, run_code, extract_image

# ── Page config ───────────────────────────────────────────
st.set_page_config(page_title="AI Data Viz Agent", page_icon="📊")
st.title("📊 AI Data Visualization Agent")
st.caption("Upload your dataset and ask questions in plain English")

# ── Sidebar ───────────────────────────────────────────────
with st.sidebar:
    st.header("⚙️ Settings")
    together_key = st.text_input("Together AI API Key", type="password")
    e2b_key      = st.text_input("E2B API Key",         type="password")

    model = st.selectbox("Model", {
        "Meta-Llama 3.3 70B": "meta-llama/Llama-3.3-70B-Instruct-Turbo",
        "DeepSeek V3":        "deepseek-ai/DeepSeek-V3",
        "Qwen 2.5 7B":        "Qwen/Qwen2.5-7B-Instruct-Turbo",
        "Meta-Llama 3.1 405B":"meta-llama/Meta-Llama-3.1-405B-Instruct-Turbo"
    })

# ── File upload ───────────────────────────────────────────
uploaded_file = st.file_uploader("📂 Upload CSV dataset", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.subheader("📋 Data Preview")
    show_full = st.checkbox("Show full dataset")
    st.dataframe(df if show_full else df.head())
    st.caption(f"Shape: {df.shape[0]} rows × {df.shape[1]} columns")

    # ── Question ──────────────────────────────────────────
    question = st.text_area(
        "💬 Ask a question about your data",
        "Show me the distribution of the first numeric column"
    )

    if st.button("🔍 Analyze"):
        if not together_key or not e2b_key:
            st.error("Please enter both API keys in the sidebar.")
            st.stop()

        # 1. Ask LLM to write the code
        with st.spinner("🧠 Thinking..."):
            full_response, python_code = ask_llm(
                api_key=together_key,
                model=model,
                user_message=question,
                dataset_path=f"./{uploaded_file.name}"
            )

        st.subheader("🤖 AI Response")
        st.write(full_response)

        if not python_code:
            st.warning("No Python code was generated.")
            st.stop()

        st.subheader("🧾 Generated Code")
        st.code(python_code, language="python")

        # 2. Run the code in E2B sandbox
        with st.spinner("⚙️ Running code in sandbox..."):
            with create_sandbox(e2b_key) as sandbox:
                upload_dataset(sandbox, uploaded_file)
                results = run_code(sandbox, python_code)

        # 3. Display results
        if results:
            st.subheader("📊 Results")
            for result in results:
                image = extract_image(result)
                if image:
                    st.image(image, caption="Generated Chart")
                elif isinstance(result, (pd.DataFrame, pd.Series)):
                    st.dataframe(result)
                else:
                    st.write(result)