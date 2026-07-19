from knowledge.providers.memory_provider import MemoryProvider
from knowledge.providers.rag_provider import RAGProvider
from knowledge.providers.web_provider import WebProvider
from capabilities.knowledge.knowledge_router import KnowledgeRouter


class KnowledgeManager:

    def __init__(self):

        self.router = KnowledgeRouter()

        self.memory_provider = MemoryProvider()

        self.provider_registry = {
            "memory": self.memory_provider,
            "rag": RAGProvider(),
            "web": WebProvider()
        }

    # -------------------------------------------------

    def retrieve(
        self,
        query,
        state
    ):

        state.add_trace(
            "Knowledge Retrieval Started"
        )

        requested_sources = self.router.route(
    query=query
)
        for source in requested_sources:

            provider = self.provider_registry.get(source)

            if provider is None:

                state.add_trace(
                    f"Unknown Knowledge Provider ({source})"
                )

                continue

            state.add_trace(
                f"Executing {source.upper()} Provider"
            )

            provider.retrieve(
                query,
                state
            )

        state.add_trace(
            "Knowledge Retrieval Completed"
        )


    # -------------------------------------------------

    def save_memory(
        self,
        user_input
    ):

        return self.memory_provider.save_memory(
            user_input
        )