import streamlit as st

from services.knowledge_service import (
    KnowledgeService
)


service = KnowledgeService()


def render_knowledge_page():

    st.header("📚 Knowledge Base")

    st.write(
        "Upload, manage and index PDF documents used by the RAG system."
    )

    st.divider()

    # =====================================================
    # Upload
    # =====================================================

    st.subheader("📤 Upload PDF")

    uploaded_file = st.file_uploader(

        "Choose a PDF",

        type=["pdf"]

    )

    if uploaded_file:

        if st.button(

            "Upload & Index",

            use_container_width=True

        ):

            with st.spinner(

                "Uploading and rebuilding index..."

            ):

                result = service.upload_document(
                    uploaded_file
                )

            st.success(

                f"{result['documents']} documents indexed."

            )

            st.rerun()

    st.divider()

    # =====================================================
    # Documents
    # =====================================================

    st.subheader("📄 Indexed Documents")

    documents = service.list_documents()

    if not documents:

        st.info(

            "No documents found."

        )

    else:

        for document in documents:

            with st.expander(

                document["name"],

                expanded=False

            ):

                col1, col2 = st.columns(2)

                with col1:

                    st.write(

                        f"**Size:** {document['size_mb']} MB"

                    )

                    st.write(

                        f"**Chunks:** {document['chunks']}"

                    )

                with col2:

                    st.write(

                        f"**Modified:** {document['modified']}"

                    )

                    st.write(

                        f"**Status:** {document['status']}"

                    )

                if st.button(

                    f"Delete {document['name']}",

                    key=document["name"],

                    type="secondary"

                ):

                    with st.spinner(

                        "Deleting document..."

                    ):

                        service.delete_document(

                            document["name"]

                        )

                    st.success(

                        "Document deleted."

                    )

                    st.rerun()

    st.divider()

    # =====================================================
    # Statistics
    # =====================================================

    st.subheader("📊 Statistics")

    total_documents = len(documents)

    total_chunks = sum(

        doc["chunks"]

        for doc in documents

    )

    col1, col2 = st.columns(2)

    col1.metric(

        "Documents",

        total_documents

    )

    col2.metric(

        "Indexed Chunks",

        total_chunks

    )

    st.divider()

    # =====================================================
    # Rebuild
    # =====================================================

    st.subheader("♻️ Rebuild Index")

    if st.button(

        "Rebuild Knowledge Index",

        use_container_width=True

    ):

        with st.spinner(

            "Rebuilding..."

        ):

            result = service.rebuild_index()

        st.success(

            f"Indexed {result['chunks']} chunks."
        )

        st.rerun()