import streamlit as st
import os
from dotenv import load_dotenv

load_dotenv()

# Set Streamlit Page Config
st.set_page_config(
    page_title="AI Data Analyst",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Glassmorphism CSS Styling
st.markdown("""
<style>
    /* Dark glassmorphism theme styling */
    .stApp {
        background-color: #0F172A;
        color: #F8FAFC;
    }
    .metric-card {
        background: rgba(30, 41, 59, 0.7);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        padding: 1.2rem;
        backdrop-filter: blur(10px);
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        text-align: center;
    }
    .metric-val {
        font-size: 1.8rem;
        font-weight: 700;
        color: #6366F1;
        margin-top: 0.25rem;
    }
    .metric-lbl {
        font-size: 0.9rem;
        color: #94A3B8;
        font-weight: 600;
    }
    .feature-box {
        background: linear-gradient(145deg, #1E293B 0%, #0F172A 100%);
        border: 1px solid rgba(99, 102, 241, 0.2);
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        transition: transform 0.2s ease;
    }
    .feature-box:hover {
        border-color: #6366F1;
        transform: translateY(-2px);
    }
    .feature-icon {
        font-size: 2rem;
        margin-bottom: 0.5rem;
    }
    .feature-title {
        font-size: 1.2rem;
        font-weight: 700;
        color: #F8FAFC;
    }
    .feature-desc {
        color: #94A3B8;
        font-size: 0.9rem;
    }
</style>
""", unsafe_allow_html=True)

# Initialize Session State
if 'df' not in st.session_state:
    st.session_state['df'] = None
if 'cleaned_df' not in st.session_state:
    st.session_state['cleaned_df'] = None
if 'dataset_name' not in st.session_state:
    st.session_state['dataset_name'] = "None"
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []
if 'ai_provider' not in st.session_state:
    st.session_state['ai_provider'] = "local"
if 'api_key' not in st.session_state:
    st.session_state['api_key'] = ""

# Render Sidebar & Header Components
from utils.components.sidebar import render_sidebar
from utils.components.header import render_header
from utils.health_score import calculate_health_score
from utils.data_summary import get_dataset_info

render_sidebar()
render_header()

df = st.session_state.get('cleaned_df')

if df is not None:
    info = get_dataset_info(df)
    health = calculate_health_score(df)

    st.subheader("📌 Dataset Snapshot")
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-lbl">Total Records</div>
                <div class="metric-val">{info.get('rows', 0):,}</div>
            </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-lbl">Total Attributes</div>
                <div class="metric-val">{info.get('cols', 0)}</div>
            </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-lbl">Data Health Score</div>
                <div class="metric-val" style="color: {'#10B981' if health.get('score', 0) >= 80 else '#F59E0B'};">{health.get('score', 0)}%</div>
            </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-lbl">Quality Grade</div>
                <div class="metric-val" style="color: #EC4899;">{health.get('grade', 'N/A').split()[0]}</div>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

st.subheader("🚀 Platform Capability Suite")

c1, c2, c3 = st.columns(3)

with c1:
    st.markdown("""
        <div class="feature-box">
            <div class="feature-icon">📊</div>
            <div class="feature-title">Data Overview</div>
            <div class="feature-desc">Interactive dataset profiling with structure analysis, column classification, missing-value tracking, key metrics and more.</div>
        </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown("""
        <div class="feature-box">
            <div class="feature-icon">📈</div>
            <div class="feature-title">Advanced Plotly Visuals</div>
            <div class="feature-desc">Dynamic scatter plots, box plots, histograms, correlation heatmaps, and customizable dark charts.</div>
        </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown("""
        <div class="feature-box">
            <div class="feature-icon">🔮</div>
            <div class="feature-title">Sales Forecasting</div>
            <div class="feature-desc">Advanced time-series forecasting to predict future sales trends and revenue performance with reliable confidence interval estimates.</div>
        </div>
    """, unsafe_allow_html=True)

c4, c5, c6 = st.columns(3)

with c4:
    st.markdown("""
        <div class="feature-box">
            <div class="feature-icon">🧠</div>
            <div class="feature-title">AI Insights & KPIs</div>
            <div class="feature-desc">Executive summaries, anomaly detection, statistical correlation findings, and actionable tips.</div>
        </div>
    """, unsafe_allow_html=True)

with c5:
    st.markdown("""
        <div class="feature-box">
            <div class="feature-icon">📄</div>
            <div class="feature-title">Executive Reports</div>
            <div class="feature-desc">Generate and download PDF executive reports, formatted Excel workbooks, and Markdown summaries.
            </div>
        </div>
    """, unsafe_allow_html=True)

with c6:
    st.markdown("""
        <div class="feature-box">
            <div class="feature-icon">🧹</div>
            <div class="feature-title">Data Cleaning</div>
            <div class="feature-desc">Automated missing value handling, duplicate removal, outlier treatment, and more for analysis-ready data.</div>
        </div>
    """, unsafe_allow_html=True)

st.markdown("---")
st.info("💡 **Quick Start Guide:** Use the left sidebar navigation menu to switch between Overview, Cleaning, Visualizations, Forecasting, Insights, Reports, Chat!")

