import streamlit as st

from ui.sidebar import render_sidebar
from ui.chat_page import render_chat
from ui.knowledge_page import render_knowledge_page
from ui.observability_page import render_observability
from ui.settings_page import render_settings

st.set_page_config(
    page_title="Agentic AI System",
    page_icon="🤖",
    layout="wide",
)

if "messages" not in st.session_state:
    st.session_state.messages = []

if "last_state" not in st.session_state:
    st.session_state.last_state = None

page = render_sidebar()

st.title("🤖 Agentic AI System")

if page == "💬 Chat":
    render_chat()

elif page == "📚 Knowledge Base":
    render_knowledge_page()

elif page == "📊 Observability":
    render_observability(st.session_state.last_state)

else:
    render_settings()