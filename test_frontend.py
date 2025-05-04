import streamlit as st
from ask_ai import get_ai_response

# Initialize session state
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

def clear_chat():
    st.session_state.chat_history = []

# Page config and styling
st.set_page_config(page_title="NBA Insights AI", layout="wide")
st.markdown("""
    <style>
        .stMarkdown {margin-bottom: 1rem;}
        .stSpinner {text-align: center;}
    </style>
""", unsafe_allow_html=True)

st.title("NBA Insights AI")

# Chat interface
with st.form(key='query_form', clear_on_submit=True):
    user_input = st.text_input(
        "Ask about NBA games, players, stats, or paste a YouTube URL:",
        placeholder="Enter your question or paste a YouTube URL...",
        key="user_input"
    )
    
    col1, col2 = st.columns([6,1])
    with col1:
        submit = st.form_submit_button("Ask AI")
    with col2:
        clear = st.form_submit_button("Clear Chat", on_click=clear_chat)
    
    if submit and user_input:
        with st.spinner("Analyzing..."):
            response = get_ai_response(user_input)
            st.session_state.chat_history.append((user_input, response))

# Display chat history with improved formatting
if st.session_state.chat_history:
    st.markdown("### Chat History")
    for query, response in reversed(st.session_state.chat_history):
        st.markdown("""
        <div style="border-left: 3px solid #0066cc; padding-left: 10px; margin: 10px 0;">
            <p><strong>You:</strong> {}</p>
            <p><strong>AI:</strong> {}</p>
        </div>
        """.format(query, response), unsafe_allow_html=True)