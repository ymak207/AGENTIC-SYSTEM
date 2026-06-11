import json

from llm.ollama_llm import OllamaLLM


PLANNER_PROMPT = """
You are a planning agent.

Rules:
- Output ONLY valid JSON
- No explanations
- Create minimal steps needed to solve the task

Every step MUST contain:
- id
- action
- description

Format:
{
  "goal": "<user goal>",
  "steps": [
    {
      "id": 1,
      "action": "<action>",
      "description": "<what to do>"
    }
  ]
}
"""


class PlannerAgent:

    def __init__(self):

        self.llm = OllamaLLM()

    # =====================================
    # PLAN VALIDATION
    # =====================================

    def _validate_plan(self, plan: dict):

        if "goal" not in plan:

            raise ValueError("Planner missing goal")

        if "steps" not in plan:

            raise ValueError("Planner missing steps")

        if not isinstance(plan["steps"], list):

            raise ValueError("Planner steps must be a list")

        if len(plan["steps"]) == 0:

            raise ValueError("Planner steps cannot be empty")

        required_fields = [
            "id",
            "action",
            "description"
        ]

        for index, step in enumerate(plan["steps"], start=1):

            for field in required_fields:

                if field not in step:

                    raise ValueError(
                        f"Step {index} missing field: {field}"
                    )

    # =====================================
    # PLAN REPAIR
    # =====================================

    def _repair_plan(
        self,
        user_goal: str,
        broken_response: str
    ) -> dict:

        repair_prompt = f"""
The planner produced an invalid plan.

User Goal:
{user_goal}

Broken Output:
{broken_response}

Fix the plan.

Return ONLY valid JSON.

Every step MUST contain:
- id
- action
- description
"""

        repaired_response = (
            self.llm.generate(repair_prompt)
            .strip()
        )

        return json.loads(repaired_response)

    # =====================================
    # PLAN GENERATION
    # =====================================

    def plan(self, user_goal: str) -> dict:

        prompt = (
            f"{PLANNER_PROMPT}\n"
            f"User goal: {user_goal}"
        )

        response = (
            self.llm.generate(prompt)
            .strip()
        )

        try:

            plan = json.loads(response)

            self._validate_plan(plan)

            return plan

        except Exception:

            repaired_plan = self._repair_plan(
                user_goal=user_goal,
                broken_response=response
            )

            self._validate_plan(repaired_plan)

            return repaired_plan