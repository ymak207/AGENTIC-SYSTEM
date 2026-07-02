import streamlit as st


def render_observability(state):

    if state is None:

        st.info(
            "Run a workflow first."
        )

        return

    st.header(
        "🔍 Workflow Observability"
    )

    # =====================================================
    # WORKFLOW ACTIVITY
    # =====================================================

    st.subheader(
        "🚀 Workflow Activity"
    )

    if state.workflow_status:

        st.dataframe(
            state.workflow_status,
            use_container_width=True,
            hide_index=True
        )

    else:

        st.info(
            "No workflow activity available."
        )

    st.divider()

    # =====================================================
    # TABS
    # =====================================================

    tab1, tab2, tab3, tab4, tab5 = st.tabs(
        [
            "📋 Plan",
            "📚 Knowledge",
            "🔍 Trace",
            "🛠 Tool Calls",
            "📊 Metrics"
        ]
    )

    # =====================================================
    # PLAN
    # =====================================================

    with tab1:

        st.subheader(
            "Generated Plan"
        )

        st.json(
            state.plan
        )

    # =====================================================
    # KNOWLEDGE
    # =====================================================

    with tab2:

        st.subheader(
            "Knowledge Retrieved"
        )

        knowledge = state.knowledge

        # ------------------------------------------

        st.markdown(
            "### 🧠 Memory"
        )

        if knowledge["memory"]:

            for memory in knowledge["memory"]:

                st.success(
                    memory
                )

        else:

            st.info(
                "No memory retrieved."
            )

        st.divider()

        # ------------------------------------------

        st.markdown(
            "### 📄 Retrieved Documents"
        )

        if knowledge["rag"]:

            for chunk in knowledge["rag"]:

                with st.expander(

                    f'{chunk["document"]} | Chunk {chunk["chunk"]} | Score {chunk["score"]:.4f}'

                ):

                    col1, col2 = st.columns(2)

                    with col1:

                        st.write(
                            f"**Chunk ID:** {chunk['chunk_id']}"
                        )

                    with col2:

                        st.write(
                            f"**Words:** {chunk['word_count']}"
                        )

                    st.text_area(

                        "Chunk Text",

                        chunk["text"],

                        height=250,

                        disabled=True,

                        key=chunk["chunk_id"]

                    )

        else:

            st.info(
                "No RAG context retrieved."
            )

    # =====================================================
    # TRACE
    # =====================================================

    with tab3:

        st.subheader(
            "Execution Timeline"
        )

        st.table(
            state.trace
        )

    # =====================================================
    # TOOL CALLS
    # =====================================================

    with tab4:

        st.subheader(
            "Tool Calls"
        )

        if state.tool_calls:

            st.json(
                state.tool_calls
            )

        else:

            st.info(
                "No tool calls."
            )

    # =====================================================
    # METRICS
    # =====================================================

    with tab5:

        st.subheader(
            "Workflow Metrics"
        )

        st.json(
            state.metrics
        )