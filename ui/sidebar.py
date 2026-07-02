import streamlit as st


def render_sidebar():

    with st.sidebar:

        st.title("🤖 Agentic AI")

        page = st.radio(

            "Navigation",

            [

                "💬 Chat",

                "📚 Knowledge Base",

                "📊 Observability",

                "⚙ Settings"

            ]

        )

    return page