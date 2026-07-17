from capabilities.capability_router import (
    CapabilityRouter
)

from capabilities.knowledge.knowledge_router import (
    KnowledgeRouter
)

from tools.router import ToolRouter

import re


class IntentRouter:

    def __init__(self):

        self.capability_router = CapabilityRouter()

        self.knowledge_router = KnowledgeRouter()

        self.tool_router = ToolRouter()

    def route(
        self,
        user_input
    ):

        result = {

            "capabilities": [],

            "knowledge_sources": [],

            "tools": [],

            "clarification_required": False,

            "clarification_question": None
        }

        # -----------------------------------
        # Tool Routing
        # -----------------------------------

        tool_result = self.tool_router.route(user_input)
        
        if tool_result.get("use_tool"):
            result["tools"].append(
                tool_result["tool_name"]
            )

        cleaned = tool_result.get(
                "tool_input",
                ""
            )
        
        if (
            tool_result.get("use_tool")
            and re.fullmatch(r"[\d\s\+\-\*/().]+", cleaned)
        ):
            planner_input = {
                "knowledge_sources": [],
                "tools": result["tools"]
            }
        
            result["capabilities"] = (
                self.capability_router.route(
                    planner_input
                )
            )
        
            return result

        # -----------------------------------
        # Knowledge Routing
        # -----------------------------------

        knowledge_sources = (
            self.knowledge_router.route(
                user_input
            )
        )

        result[
            "knowledge_sources"
        ] = knowledge_sources

        

        

        # -----------------------------------
        # Capability Routing
        # -----------------------------------

        planner_input = {

            "knowledge_sources":
                knowledge_sources,

            "tools":
                result["tools"]
        }

        result[
            "capabilities"
        ] = self.capability_router.route(
            planner_input
        )

        return result