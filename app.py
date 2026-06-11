import streamlit as st

from orchestrator.workflow import run_workflow

# =====================================
# PAGE CONFIG
# =====================================

st.set_page_config(
    page_title="Agentic AI System",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 Agentic AI System")

# =====================================
# SESSION STATE
# =====================================

if "messages" not in st.session_state:

    st.session_state.messages = []

# =====================================
# DISPLAY CHAT HISTORY
# =====================================

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])

# =====================================
# CHAT INPUT
# =====================================

user_input = st.chat_input(
    "Ask something..."
)

# =====================================
# PROCESS REQUEST
# =====================================

if user_input:

    # user message

    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_input
        }
    )

    with st.chat_message("user"):

        st.markdown(user_input)

    # assistant processing

    with st.chat_message("assistant"):

        with st.spinner("Thinking..."):

            response = run_workflow(
                user_input
            )

            st.markdown(response)

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": response
        }
    )