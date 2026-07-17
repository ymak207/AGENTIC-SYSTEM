from capabilities.base_capability import (
    BaseCapability
)

from capabilities.knowledge.knowledge_router import (
    KnowledgeRouter
)

from knowledge.providers.memory_provider import (
    MemoryProvider
)

from knowledge.providers.rag_provider import (
    RAGProvider
)

from knowledge.providers.web_provider import (
    WebProvider
)


class KnowledgeCapability(
    BaseCapability
):

    def __init__(self):

        self.router = KnowledgeRouter()

        self.memory = MemoryProvider()

        self.rag = RAGProvider()

        self.web = WebProvider()

    @property
    def name(self):

        return "knowledge"

    def execute(
        self,
        request,
        context
    ):

        state = context.state

        query = request.get(
            "query",
            ""
        )

        context.trace(
            "Knowledge Capability Executed"
        )

        sources = self.router.route(
            query
        )

        if "memory" in sources:

            self.memory.retrieve(
                query,
                state
            )

        if "rag" in sources:

            self.rag.retrieve(
                query,
                state
            )

        if "web" in sources:

            self.web.retrieve(
                query,
                state
            )

        return {

            "sources": sources,

            "memory":
                state.knowledge["memory"],

            "rag":
                state.knowledge["rag"],

            "web":
                state.knowledge["web"]
        }