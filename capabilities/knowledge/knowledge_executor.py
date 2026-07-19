from knowledge.knowledge_manager import KnowledgeManager


class KnowledgeExecutor:

    def __init__(self):

        self.manager = KnowledgeManager()

    def execute(
        self,
        step,
        state,
        user_goal
    ):

        state.add_trace(
            f"Knowledge capability started: {step['action']}"
        )

        self.manager.retrieve(
            query=user_goal,
            state=state
        )

        state.add_trace(
            f"Knowledge capability completed: {step['action']}"
        )