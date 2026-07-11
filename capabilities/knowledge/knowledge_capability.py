from capabilities.base_capability import (
    BaseCapability
)


class KnowledgeCapability(BaseCapability):

    @property
    def name(self):

        return "knowledge"

    def execute(

        self,

        request,

        context

    ):

        state = context.state

        result = {

            "memory":
                state.knowledge["memory"],

            "rag":
                state.knowledge["rag"],

            "web":
                state.knowledge["web"]
        }

        context.trace(

            "Knowledge Capability Executed"

        )

        return result