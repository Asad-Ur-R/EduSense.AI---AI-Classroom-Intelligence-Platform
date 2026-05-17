import streamlit as st
import sys
sys.path.insert(0, '.')
from utils.page_guard import require_data
from agents.chatbot_agent import ask_chatbot

st.set_page_config(page_title="EduSense AI Chat", page_icon="🤖", layout="wide")
require_data()

st.title("🤖 EduSense AI Assistant")
st.caption("Ask anything about your students in plain English")

with st.expander("💡 Example questions you can ask"):
    st.markdown("""
- Who are the High Risk students in Grade 10?
- Which subject has the lowest average quiz score?
- Show me students with attendance below 60%
- Who has the highest risk score?
- How many students are missing more than 3 assignments?
- What are the most common weak topics?
- Show top 5 students by overall score
- Which grade has the most at-risk students?
""")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

user_input = st.chat_input("Ask about your students...")

if user_input:
    with st.chat_message("user"):
        st.markdown(user_input)
    st.session_state.chat_history.append({"role": "user", "content": user_input})

    with st.chat_message("assistant"):
        with st.spinner("Analysing student data..."):
            response = ask_chatbot(user_input, st.session_state.chat_history)
        st.markdown(response)
    st.session_state.chat_history.append({"role": "assistant", "content": response})

if st.session_state.chat_history:
    if st.button("🗑️ Clear Chat"):
        st.session_state.chat_history = []
        st.rerun()
