from capabilities.knowledge.memory.memory_router import MemoryRouter
from capabilities.knowledge.rag.rag_router import RagRouter


class KnowledgeExecutor:

    def __init__(self):

        self.memory_router = MemoryRouter()

        self.rag_router = RagRouter()

    def execute(
        self,
        step,
        state,
        user_goal
    ):

        state.add_trace(
            f"Knowledge capability started: {step['action']}"
        )

        memory = self.memory_router.retrieve(
            user_goal
        )

        if memory:

            state.knowledge["memory"] = memory

            state.add_trace(
                f"Memory Retrieved ({len(memory)})"
            )

        rag = self.rag_router.retrieve(
            user_goal
        )

        if rag:

            state.knowledge["rag"] = rag

            state.add_trace(
                f"RAG Retrieved ({len(rag)})"
            )

        state.add_trace(
            f"Knowledge capability completed: {step['action']}"
        )