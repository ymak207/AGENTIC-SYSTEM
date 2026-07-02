from memory.memory_agent import MemoryAgent

from knowledge.rag_vector_store import (
    RAGVectorStore
)


class KnowledgeManager:

    def __init__(self):

        self.memory = MemoryAgent()

        self.rag = RAGVectorStore()

    def retrieve(
        self,
        query: str,
        state
    ):

        state.add_trace(
            "Knowledge Retrieval Started"
        )

        # --------------------------
        # MEMORY
        # --------------------------

        memory_context = (
            self.memory.get_relevant_memory(
                query
            )
        )

        state.knowledge["memory"] = (
            memory_context
        )

        state.metrics[
            "memories_loaded"
        ] = len(memory_context)

        state.add_trace(
            f"Memory Retrieved ({len(memory_context)})"
        )

        # --------------------------
        # RAG
        # --------------------------

        rag_context = (
            self.rag.search(
                query,
                top_k=5
            )
        )

        state.knowledge["rag"] = (
            rag_context
        )

        state.add_trace(
            f"RAG Retrieved ({len(rag_context)})"
        )

        state.add_trace(
            "Knowledge Retrieval Completed"
        )

    def save_memory(
        self,
        user_input: str
    ):

        keywords = [

            "my name is",

            "i am",

            "i work as",

            "i am learning",

            "i like"

        ]

        for keyword in keywords:

            if keyword in user_input.lower():

                self.memory.save_fact(
                    user_input
                )

                return 1

        return 0