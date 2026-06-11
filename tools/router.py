import json
import re

from llm.ollama_llm import OllamaLLM
from tools.tool_registry import TOOLS


class ToolRouter:

    def __init__(self):

        self.llm = OllamaLLM()

    def route(self, user_goal: str) -> dict:

        goal_lower = user_goal.lower().strip()

        # =====================================
        # STEP 1: CLEAN INPUT
        # =====================================

        cleaned_goal = (
            goal_lower
            .replace("calculate", "")
            .replace("what is", "")
            .strip()
        )

        # remove ending punctuation
        cleaned_goal = re.sub(
            r"[?.!,;:]+$",
            "",
            cleaned_goal
        ).strip()

        # =====================================
        # STEP 2: DETERMINISTIC ROUTING
        # =====================================

        math_pattern = r"^[0-9\s\+\-\*\/\(\)\.]+$"

        if re.match(math_pattern, cleaned_goal):

            return {
                "use_tool": True,
                "tool_name": "calculator",
                "tool_input": cleaned_goal,
                "routing_type": "deterministic"
            }

        # =====================================
        # STEP 3: LLM ROUTING
        # =====================================

        tool_prompt = f"""
You are a tool routing agent.

Available tools:
{list(TOOLS.keys())}

User request:
{user_goal}

Decide whether a tool is needed.

Return ONLY valid JSON.

Format:
{{
    "use_tool": true or false,
    "tool_name": "tool name",
    "tool_input": "input for tool"
}}
"""

        tool_response = self.llm.generate(tool_prompt).strip()

        try:

            tool_decision = json.loads(tool_response)

            tool_decision["routing_type"] = "llm"

            if not tool_decision.get("use_tool"):

                tool_decision["tool_name"] = None
                tool_decision["tool_input"] = None

            return tool_decision

        except Exception:

            return {
                "use_tool": False,
                "tool_name": None,
                "tool_input": None,
                "routing_type": "fallback"
            }