import streamlit as st

from orchestrator.workflow import run_workflow


def render_chat():

    for message in st.session_state.messages:

        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    prompt = st.chat_input("Ask something...")

    if not prompt:
        return

    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt,
        }
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):

        with st.spinner("Running workflow..."):

            state = run_workflow(prompt)

        st.markdown(state.final_answer)

        with st.expander("Workflow Summary", expanded=False):

            latest_event = (
                state.trace[-1]["event"]
                if getattr(state, "trace", None)
                and len(state.trace) > 0
                else "Completed"
            )
        
            c1, c2, c3, c4 = st.columns(4)
        
            with c1:
                st.metric(
                    "Workflow",
                    latest_event,
                )
        
            with c2:
                st.metric(
                    "LLM Calls",
                    state.metrics.get("llm_calls", 0),
                )
        
            with c3:
                st.metric(
                    "Workflow Time",
                    f'{state.metrics.get("workflow_seconds", 0):.2f}s',
                )
        
            with c4:
                st.metric(
                    "Planner Repairs",
                    state.metrics.get("planner_repairs", 0),
                )



    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": state.final_answer,
        }
    )

    st.session_state.last_state = state

    st.rerun()