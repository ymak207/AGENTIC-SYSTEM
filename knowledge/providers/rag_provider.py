from knowledge.rag_vector_store import (
    RAGVectorStore
)

from knowledge.providers.base_provider import (
    BaseKnowledgeProvider
)


class RAGProvider(BaseKnowledgeProvider):

    def __init__(self):

        self.vector_store = RAGVectorStore()

    def retrieve(
        self,
        query,
        state
    ):

        context = self.vector_store.search(

            query,

            top_k=5

        )

        state.knowledge["rag"] = context

        state.add_trace(

            f"RAG Retrieved ({len(context)})"

        )