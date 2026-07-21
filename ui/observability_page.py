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
            "📋 Planner",
            "📚 Knowledge",
            "🧮 Compute",
            "🔍 Trace",
            "📊 Metrics",
        ]
    )

    # =====================================================
    # PLAN
    # =====================================================

    with tab1:

        st.subheader("Planner Output")
    
        st.json(state.plan)
    
        if state.metrics.get("planner_repairs", 0):
    
            st.warning(
                f'Planner Repairs : {state.metrics["planner_repairs"]}'
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
        
        st.divider()

        st.markdown("### 🌐 Web")
        
        if state.knowledge["web"]:
        
            for page in state.knowledge["web"]:
        
                with st.expander(page["title"]):
        
                    st.write(page["url"])
        
                    st.write(page["content"])
        
        else:
        
            st.info("No web results.")

    # =====================================================
    # TRACE
    # =====================================================

    with tab4:

        st.subheader(
            "Execution Timeline"
        )

        st.dataframe(
                state.trace,
                use_container_width=True,
                hide_index=True,
            )

    # =====================================================
    # COMPUTE
    # =====================================================
    
    with tab3:
    
        st.subheader("Compute Results")
    
        if state.compute_results:
    
            st.dataframe(
                state.compute_results,
                use_container_width=True,
                hide_index=True,
            )
    
        else:
    
            st.info("No compute execution.")

    # =====================================================
    # METRICS
    # =====================================================

    with tab5:

        m = state.metrics
    
        c1, c2, c3 = st.columns(3)
    
        c1.metric(
            "Planner",
            f"{m.get('planner_seconds', 0):.2f}s",
        )
    
        c2.metric(
            "Executor",
            f"{m.get('executor_seconds', 0):.2f}s",
        )
    
        c3.metric(
            "Reviewer",
            f"{m.get('reviewer_seconds', 0):.2f}s",
        )
    
        c1, c2, c3 = st.columns(3)
    
        c1.metric(
            "Workflow",
            f"{m.get('workflow_seconds', 0):.2f}s",
        )
    
        c2.metric(
            "LLM Calls",
            m.get("llm_calls", 0),
        )
    
        c3.metric(
            "Planner Repairs",
            m.get("planner_repairs", 0),
        )
    
        st.divider()
    
        st.json(m)