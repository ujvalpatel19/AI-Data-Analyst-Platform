import streamlit as st
from utils.ai_insights import generate_ai_insights
from utils.components.sidebar import render_sidebar
from utils.components.header import render_header

st.set_page_config(page_title="AI Insights - AI Data Analyst", page_icon="🧠", layout="wide")

render_sidebar()
render_header(title="AI-Powered Insights & Executive KPIs", subtitle="Automated Statistical Pattern Recognition & Strategic Recommendations")

df = st.session_state.get('cleaned_df')

if df is None or df.empty:
    st.warning("⚠️ No dataset loaded. Please upload a dataset from the sidebar first.")
    st.stop()

ai_provider = st.session_state.get('ai_provider', 'local')
api_key = st.session_state.get('api_key', '')

with st.spinner("Generating AI Insights..."):
    insights_data = generate_ai_insights(df, provider=ai_provider, api_key=api_key)

# Render KPI Scorecards
metrics = insights_data.get("key_metrics", [])
if metrics:
    st.subheader("🎯 Key Performance Indicators (KPIs)")
    cols = st.columns(len(metrics))
    for idx, metric in enumerate(metrics):
        cols[idx].metric(label=metric.get("label", "Metric"), value=metric.get("value", "0"), delta=metric.get("sub", None))

st.markdown("---")

col_a, col_b = st.columns([1, 1])

with col_a:
    st.subheader("💡 Automated Data Insights")
    st.info(f"**Executive Summary:**\n\n{insights_data.get('summary', '')}")
    
    st.markdown("#### Key Observations & Patterns:")
    for ins in insights_data.get("insights", []):
        st.markdown(f"• {ins}")

with col_b:
    st.subheader("🎯 Strategic Recommendations")
    recs = insights_data.get("recommendations", [])
    for idx, rec in enumerate(recs, 1):
        st.success(f"**Action {idx}:** {rec}")
