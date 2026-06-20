# app.py
# PURPOSE: Streamlit UI only — no business logic here
import json
import streamlit as st
from agent import get_agent
from coverage import compute_local_breakdown, safe_number
from utils import format_currency, extract_json, parse_percentage
from datetime import datetime

# ── Page config ───────────────────────────────────────────
st.set_page_config(
    page_title="Life Insurance Advisor",
    page_icon="🛡️",
    layout="centered"
)
st.title("🛡️ Life Insurance Coverage Advisor")
st.caption("Powered by AI — calculates your coverage and finds real products")

# ── Sidebar: API keys ─────────────────────────────────────
with st.sidebar:
    st.header("🔑 API Keys")
    openai_key    = st.text_input("OpenAI API Key",    type="password")
    firecrawl_key = st.text_input("Firecrawl API Key", type="password")
    e2b_key       = st.text_input("E2B API Key",       type="password")

# ── User input form ───────────────────────────────────────
st.subheader("Tell us about yourself")

with st.form("coverage_form"):
    col1, col2 = st.columns(2)

    with col1:
        age           = st.number_input("Age", min_value=18, max_value=85, value=35)
        annual_income = st.number_input("Annual Income", min_value=0.0, value=85000.0, step=1000.0)
        dependents    = st.number_input("Dependents", min_value=0, max_value=10, value=2)
        location      = st.text_input("Country / State", value="United States")

    with col2:
        total_debt    = st.number_input("Total Debt (incl. mortgage)", min_value=0.0, value=200000.0, step=5000.0)
        savings       = st.number_input("Savings & Investments", min_value=0.0, value=50000.0, step=5000.0)
        existing_cover = st.number_input("Existing Life Insurance", min_value=0.0, value=100000.0, step=5000.0)
        currency      = st.selectbox("Currency", ["USD", "EUR", "GBP", "CAD", "AUD", "INR"])

    income_replacement_years = st.selectbox(
        "Income Replacement Years", [5, 10, 15], index=1
    )

    submitted = st.form_submit_button("🔍 Calculate & Find Products")

# ── On form submit ────────────────────────────────────────
if submitted:
    if not all([openai_key, firecrawl_key, e2b_key]):
        st.error("Please enter all 3 API keys in the sidebar.")
        st.stop()

    # Build client profile
    profile = {
        "age": age,
        "annual_income": annual_income,
        "dependents": dependents,
        "location": location,
        "total_debt": total_debt,
        "available_savings": savings,
        "existing_life_insurance": existing_cover,
        "income_replacement_years": income_replacement_years,
        "currency": currency,
        "request_timestamp": datetime.utcnow().isoformat(),
    }

    # Step 1: Show local math immediately
    st.subheader("📊 Coverage Calculation")
    local = compute_local_breakdown(profile, real_rate=0.02)

    st.metric(
        label="Estimated Coverage Needed",
        value=format_currency(local["recommended"], currency)
    )

    st.table({
        "Step": [
            "Annual income",
            "Annuity factor (10yr @ 2%)",
            "Discounted income",
            "+ Total debt",
            "- Savings",
            "- Existing cover",
            "= Coverage needed"
        ],
        "Amount": [
            format_currency(local["income"], currency),
            f"{local['annuity_factor']:.3f}",
            format_currency(local["discounted_income"], currency),
            format_currency(local["debt"], currency),
            format_currency(savings, currency),
            format_currency(existing_cover, currency),
            format_currency(local["recommended"], currency),
        ]
    })

    # Step 2: Ask agent to search for products
    st.subheader("🤖 Finding Insurance Products...")
    advisor = get_agent(openai_key, firecrawl_key, e2b_key)

    user_prompt = (
        "Calculate coverage and find term life insurance products "
        "for this client:\n"
        f"{json.dumps(profile)}"
    )

    with st.spinner("Agent is searching for products..."):
        response = advisor.run(user_prompt, stream=False)

    parsed = extract_json(response.content if response else "")

    if not parsed:
        st.warning("Agent returned unexpected response.")
        with st.expander("Raw agent output"):
            st.write(response.content if response else "empty")
    else:
        # Show product recommendations
        recommendations = parsed.get("recommendations", [])
        if recommendations:
            st.subheader("🏆 Top Insurance Products Found")
            for i, option in enumerate(recommendations, 1):
                st.markdown(f"**{i}. {option.get('name', 'Unknown')}**")
                st.write(option.get('summary', ''))
                link = option.get('link')
                if link:
                    st.markdown(f"[View details]({link})")
                st.markdown("---")

        if parsed.get("research_notes"):
            st.caption(parsed["research_notes"])

        with st.expander("Full agent response JSON"):
            st.json(parsed)

st.divider()
st.caption("For educational use only. Consult a licensed financial advisor.")