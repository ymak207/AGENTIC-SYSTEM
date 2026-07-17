import re


class ToolRouter:

    def route(
        self,
        user_goal: str
    ) -> dict:

        goal_lower = user_goal.lower().strip()

        # =====================================
        # STEP 1: CLEAN INPUT
        # =====================================

        cleaned_goal = re.sub(
            r"\b(calculate|compute|what is)\b",
            "",
            goal_lower,
            flags=re.IGNORECASE
        ).strip()

        cleaned_goal = re.sub(
            r"[?.!,;:]+$",
            "",
            cleaned_goal
        ).strip()

        # =====================================
        # STEP 2: MATH DETECTION
        # =====================================

        math_pattern = r"^[\d\s\+\-\*/().]+$"

        math_words = [

            "plus",
            "minus",
            "add",
            "subtract",
            "multiply",
            "multiplied",
            "times",
            "into",
            "divide",
            "divided",
            "calculate"

        ]

        contains_math_words = any(
            word in goal_lower
            for word in math_words
        )

        if (
            re.fullmatch(math_pattern, cleaned_goal)
            or contains_math_words
        ):

            return {
                "use_tool": True,
                "tool_name": "calculator",
                "tool_input": cleaned_goal,
                "routing_type": "deterministic"
            }

        # =====================================
        # NO TOOL REQUIRED
        # =====================================

        return {
            "use_tool": False,
            "tool_name": None,
            "tool_input": None,
            "routing_type": "deterministic"
        }