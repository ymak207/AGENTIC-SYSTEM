import streamlit as st

from orchestrator.workflow import run_workflow

from ui.sidebar import render_sidebar
from ui.chat_page import render_chat
from ui.knowledge_page import render_knowledge_page
from ui.observability_page import render_observability
from ui.settings_page import render_settings


# =====================================
# PAGE CONFIG
# =====================================

st.set_page_config(

    page_title="Agentic AI System",

    page_icon="🤖",

    layout="wide"

)

# =====================================
# SESSION STATE
# =====================================

if "messages" not in st.session_state:

    st.session_state.messages = []

if "last_state" not in st.session_state:

    st.session_state.last_state = None

# =====================================
# SIDEBAR
# =====================================

page = render_sidebar()

# =====================================
# CHAT PAGE
# =====================================

if page == "💬 Chat":

    st.title("🤖 Agentic AI System")

    for message in st.session_state.messages:

        with st.chat_message(message["role"]):

            st.markdown(
                message["content"]
            )

    user_input = st.chat_input(
        "Ask something..."
    )

    if user_input:

        st.session_state.messages.append(
            {
                "role": "user",
                "content": user_input
            }
        )

        with st.chat_message("user"):

            st.markdown(user_input)

        with st.chat_message("assistant"):

            with st.spinner(
                "Running workflow..."
            ):

                state = run_workflow(
                    user_input
                )

                st.markdown(
                    state.final_answer
                )

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": state.final_answer
            }
        )

        st.session_state.last_state = state

        st.rerun()

# =====================================
# KNOWLEDGE BASE
# =====================================

elif page == "📚 Knowledge Base":

    st.title("🤖 Agentic AI System")

    render_knowledge_page()

# =====================================
# OBSERVABILITY
# =====================================

elif page == "📊 Observability":

    st.title("🤖 Agentic AI System")

    render_observability(
        st.session_state.last_state
    )

# =====================================
# SETTINGS
# =====================================

else:

    st.title("🤖 Agentic AI System")

    render_settings()