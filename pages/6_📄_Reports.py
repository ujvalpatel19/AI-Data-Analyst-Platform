import streamlit as st
from utils.health_score import calculate_health_score
from utils.ai_insights import generate_ai_insights
from reports.pdf_report import generate_pdf_report
from reports.report_generator import generate_excel_report, generate_markdown_report
from utils.components.sidebar import render_sidebar
from utils.components.header import render_header

st.set_page_config(page_title="Reports - AI Data Analyst", page_icon="📄", layout="wide")

render_sidebar()
render_header(title="Report Generator & Exporter", subtitle="Generate Professional Executive PDF, Excel & Markdown Reports")

df = st.session_state.get('cleaned_df')
dataset_name = st.session_state.get('dataset_name', 'dataset.csv')
ai_provider = st.session_state.get('ai_provider', 'local')
api_key = st.session_state.get('api_key', '')

if df is None or df.empty:
    st.warning("⚠️ No dataset loaded. Please upload a dataset from the sidebar first.")
    st.stop()

health_data = calculate_health_score(df)
insights_data = generate_ai_insights(df, provider=ai_provider, api_key=api_key)

st.subheader("📦 Available Report Formats")

c1, c2, c3 = st.columns(3)

with c1:
    st.markdown("### 📄 Executive PDF Report")
    st.write("Complete executive report formatted with ReportLab containing health grades, KPI scorecards, insights, and recommendations.")
    pdf_buffer = generate_pdf_report(dataset_name, health_data, insights_data)
    st.download_button(
        label="📥 Download PDF Report",
        data=pdf_buffer,
        file_name=f"Executive_Report_{dataset_name}.pdf",
        mime="application/pdf",
        use_container_width=True
    )

with c2:
    st.markdown("### 📊 Formatted Excel Report")
    st.write("Multi-tab Excel workbook containing cleaned dataset, data health audit, and KPI metric summary tabs.")
    excel_buffer = generate_excel_report(df, health_data, insights_data)
    st.download_button(
        label="📥 Download Excel Workbook",
        data=excel_buffer,
        file_name=f"Data_Report_{dataset_name}.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        use_container_width=True
    )

with c3:
    st.markdown("### 📝 Markdown Summary")
    st.write("Lightweight Markdown document suitable for copying into Notion, GitHub, Slack, or documentation systems.")
    md_text = generate_markdown_report(dataset_name, health_data, insights_data)
    st.download_button(
        label="📥 Download Markdown (.md)",
        data=md_text,
        file_name=f"Report_{dataset_name}.md",
        mime="text/markdown",
        use_container_width=True
    )

st.markdown("---")
st.subheader("👀 Markdown Preview")
st.markdown(md_text)
