import streamlit as st

def render_header(title="AI Data Analyst", subtitle="Automated Data Analytics, Visualizations & Insights"):
    """Renders a sleek top header banner."""
    st.markdown("""
        <style>
        .header-container {
            background: linear-gradient(135deg, #1E1E2E 0%, #2A2A40 100%);
            padding: 1.5rem 2rem;
            border-radius: 12px;
            margin-bottom: 1.5rem;
            border: 1px solid rgba(255, 255, 255, 0.08);
            box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.3);
        }
        .header-title {
            color: #FFFFFF;
            font-size: 2rem;
            font-weight: 700;
            margin: 0;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        .header-subtitle {
            color: #94A3B8;
            font-size: 1rem;
            margin-top: 0.25rem;
            margin-bottom: 0;
        }
        .dataset-badge {
            display: inline-block;
            background: rgba(99, 102, 241, 0.2);
            color: #A5B4FC;
            border: 1px solid rgba(99, 102, 241, 0.4);
            padding: 0.2rem 0.75rem;
            border-radius: 20px;
            font-size: 0.85rem;
            font-weight: 600;
            margin-top: 0.5rem;
        }
        </style>
    """, unsafe_allow_html=True)

    dataset_name = st.session_state.get('dataset_name', 'No dataset loaded')
    
    st.markdown(f"""
        <div class="header-container">
            <h1 class="header-title">🤖 {title}</h1>
            <p class="header-subtitle">{subtitle}</p>
            <div class="dataset-badge">📂 Active Dataset: {dataset_name}</div>
        </div>
    """, unsafe_allow_html=True)
