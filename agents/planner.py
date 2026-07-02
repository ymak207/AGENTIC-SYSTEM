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
        broken_response: str,
        state=None
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
    
        if state:
    
            state.metrics["llm_calls"] += 1
    
        repaired_response = (
            self.llm.generate(repair_prompt)
            .strip()
        )
    
        return json.loads(repaired_response)

    # =====================================
    # PLAN GENERATION
    # =====================================

    # =====================================
    # OBSERVABILITY CHANGE #1
    # Added state parameter
    # =====================================

    def plan(
        self,
        user_goal: str,
        state=None
    ) -> dict:

        # =====================================
        # OBSERVABILITY CHANGE #2
        # Planner start event
        # =====================================

        if state:

            state.add_trace(
                "Planner Started"
            )

        memory_text = ""

        if state and state.knowledge["memory"]:

            memory_text = (
                "\nKnown User Memory:\n"
                + "\n".join(
                    state.knowledge["memory"]
                )
                + "\n"
            )
        
        prompt = (
            f"{PLANNER_PROMPT}\n"
            f"{memory_text}\n"
            f"User goal: {user_goal}"
        )


        if state:

          state.metrics["llm_calls"] += 1

        response = (self.llm.generate(prompt).strip())

        # =====================================
        # OBSERVABILITY CHANGE #3
        # LLM response received
        # =====================================

        if state:

            state.add_trace(
                "Planner Response Received"
            )

        try:

            plan = json.loads(response)

            # =====================================
            # OBSERVABILITY CHANGE #4
            # JSON parsed successfully
            # =====================================

            if state:

                state.add_trace(
                    "Planner JSON Parsed"
                )

            self._validate_plan(plan)

            # =====================================
            # OBSERVABILITY CHANGE #5
            # Validation successful
            # =====================================

            if state:

                state.add_trace(
                    f"Plan Validated ({len(plan['steps'])} steps)"
                )

                state.plan = plan

                state.add_trace(
                    "Planner Completed"
                )

            return plan

        except Exception as e:

            # =====================================
            # OBSERVABILITY CHANGE #6
            # Validation failure
            # =====================================

            if state:

                state.add_trace(
                    f"Validation Failed: {str(e)}"
                )

                state.add_trace(
                    "Repair Started"
                )

            repaired_plan = self._repair_plan(
              user_goal=user_goal,
              broken_response=response,
              state=state)

            self._validate_plan(repaired_plan)

            # =====================================
            # OBSERVABILITY CHANGE #7
            # Repair success
            # =====================================

            if state:

                state.add_trace(
                    "Repair Successful"
                )

                state.plan = repaired_plan

                state.add_trace(
                    "Planner Completed"
                )

            return repaired_plan