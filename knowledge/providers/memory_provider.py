from memory.memory_agent import MemoryAgent

from knowledge.providers.base_provider import (
    BaseKnowledgeProvider
)


class MemoryProvider(BaseKnowledgeProvider):

    def __init__(self):

        self.memory = MemoryAgent()

    def retrieve(
        self,
        query,
        state
    ):

        context = self.memory.get_relevant_memory(
            query
        )

        state.knowledge["memory"] = context

        state.metrics[
            "memories_loaded"
        ] = len(context)

        state.add_trace(
            f"Memory Retrieved ({len(context)})"
        )

    def save_memory(
        self,
        user_input
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