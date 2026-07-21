import streamlit as st


def render_sidebar():

    with st.sidebar:

        st.title("🤖 Agentic AI")

        st.caption("Enterprise Agentic Workflow")

        page = st.radio(
            "Navigation",
            [
                "💬 Chat",
                "📚 Knowledge Base",
                "📊 Observability",
                "⚙ Settings",
            ],
        )

        st.divider()

        if st.session_state.last_state:

            metrics = st.session_state.last_state.metrics

            st.metric(
                "LLM Calls",
                metrics.get("llm_calls", 0),
            )

            st.metric(
                "Planner Repairs",
                metrics.get("planner_repairs", 0),
            )

            st.metric(
                "Workflow Time",
                f'{metrics.get("workflow_seconds",0):.2f}s',
            )

    return page