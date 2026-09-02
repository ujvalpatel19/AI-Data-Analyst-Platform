import streamlit as st
from utils.ai_chat import ask_data_chat
from utils.components.sidebar import render_sidebar
from utils.components.header import render_header

st.set_page_config(page_title="Chat with Data - AI Data Analyst", page_icon="💬", layout="wide")

render_sidebar()
render_header(title="Chat with Data", subtitle="Ask Questions in Natural Language & Query Your Dataset")

df = st.session_state.get('cleaned_df')
ai_provider = st.session_state.get('ai_provider', 'local')
api_key = st.session_state.get('api_key', '')

if df is None or df.empty:
    st.warning("⚠️ No dataset loaded. Please upload a dataset from the sidebar first.")
    st.stop()

# Initialize Chat History
if 'chat_messages' not in st.session_state:
    st.session_state['chat_messages'] = [
        {"role": "assistant", "content": "👋 Hi! I am your AI Data Assistant. Ask me anything about your dataset!"}
    ]

# Preset quick suggestion prompts
st.markdown("#### 💡 Quick Questions:")
chip_col1, chip_col2, chip_col3, chip_col4 = st.columns(4)

q_prompt = None
if chip_col1.button("📊 What is the total sales?"):
    q_prompt = "What is the total sales?"
elif chip_col2.button("🏆 Which category is highest?"):
    q_prompt = "Which category generated the highest profit?"
elif chip_col3.button("📈 What is the average discount?"):
    q_prompt = "What is the average discount?"
elif chip_col4.button("🔢 How many total records?"):
    q_prompt = "How many total records?"

# Display message transcript
for msg in st.session_state['chat_messages']:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User Chat Input
user_input = st.chat_input("Ask a question about your uploaded dataset...")
if q_prompt:
    user_input = q_prompt

if user_input:
    # Append User Message
    st.session_state['chat_messages'].append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Process Assistant Response
    with st.chat_message("assistant"):
        with st.spinner("Analyzing dataset..."):
            ans = ask_data_chat(df, user_input, provider=ai_provider, api_key=api_key)
            st.markdown(ans)
            st.session_state['chat_messages'].append({"role": "assistant", "content": ans})
