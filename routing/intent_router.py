from capabilities.capability_router import CapabilityRouter
from capabilities.knowledge.knowledge_router import KnowledgeRouter
from tools.router import ToolRouter


class IntentRouter:

    def __init__(self):

        self.capability_router = CapabilityRouter()

        self.knowledge_router = KnowledgeRouter()

        self.tool_router = ToolRouter()

    def route(
        self,
        user_input
    ):

        intent = {

            "knowledge_required": self.knowledge_router.requires_knowledge(
                user_input
            ),

            "compute_required": self.tool_router.route(
                user_input
            )["use_tool"]

        }

        capabilities = self.capability_router.route(
            intent
        )

        return {

            "capabilities": capabilities

        }