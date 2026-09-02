import streamlit as st
import os
from utils.data_loader import load_data

def render_sidebar():
    """Renders the sidebar navigation and configuration panel."""
    with st.sidebar:
        st.title("⚙️ Data Settings")
        
        st.markdown("---")
        st.subheader("📂 1. Dataset Selection")

        uploaded_file = st.file_uploader("Upload CSV or Excel file", type=["csv", "xlsx", "xls"])

        reset_data = st.button("🔄 Reset", use_container_width=True)

        if reset_data:
            st.session_state['df'] = None
            st.session_state['cleaned_df'] = None
            st.session_state['dataset_name'] = "None"
            st.rerun()

        if uploaded_file is not None:
            df = load_data(uploaded_file)
            if df is not None:
                st.session_state['df'] = df
                st.session_state['cleaned_df'] = df.copy()
                st.session_state['dataset_name'] = uploaded_file.name
                st.sidebar.success(f"Loaded {uploaded_file.name}!")
        st.markdown("---")
        st.subheader("🧠 2. AI Intelligence Engine")

        ai_provider = st.selectbox(
            "Select AI Engine",
            ["local", "openai", "gemini"],
            format_func=lambda x: {
                "local": "⚡ Local Offline Engine (Free)",
                "openai": "🤖 OpenAI (GPT-4o)",
                "gemini": "✨ Google Gemini (Flash)"
            }[x]
        )
        st.session_state['ai_provider'] = ai_provider

        api_key = ""

        if ai_provider == "openai":
            api_key = os.getenv("OPENAI_API_KEY", "")

            if api_key:
                st.success("✅ OpenAI API key loaded ")
            else:
                st.warning("⚠️ OPENAI_API_KEY not found in .env")

        elif ai_provider == "gemini":
            api_key = os.getenv("GEMINI_API_KEY", "")

            if api_key:
                st.success("✅ Gemini API key loaded ")
            else:
                st.warning("⚠️ GEMINI_API_KEY not found in .env")

        else:
            st.info("⚡ Running with Local Offline Engine")

        st.session_state['api_key'] = api_key

        st.markdown("---")
        st.markdown("""
        
        """, unsafe_allow_html=True)
