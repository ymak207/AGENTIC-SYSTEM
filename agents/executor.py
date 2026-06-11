from llm.ollama_llm import OllamaLLM

from tools.router import ToolRouter
from tools.tool_executor import ToolExecutor


class ExecutorAgent:

    def __init__(self):

        self.llm = OllamaLLM()

        self.router = ToolRouter()

        self.tool_executor = ToolExecutor()

    def execute(self, plan: dict, state, user_goal: str):

        # =====================================
        # STEP 1: ROUTE REQUEST
        # =====================================

        tool_decision = self.router.route(user_goal)

        # =====================================
        # STEP 2: EXECUTE TOOL
        # =====================================

        if tool_decision.get("use_tool"):

            execution_result = self.tool_executor.execute(
                tool_name=tool_decision["tool_name"],
                tool_input=tool_decision["tool_input"]
            )

            if execution_result["success"]:

                state.final_answer = (
                    f"Tool Used: "
                    f"{execution_result['tool_name']}\n"
                    f"Result: "
                    f"{execution_result['result']}"
                )
                return  
            
            state.final_answer = (
                f"Tool Used: "
                f"{execution_result['tool_name']}\n"
                f"Error: "
                f"{execution_result['error']}"
            )

            return

        # =====================================
        # STEP 3: RETRY FEEDBACK
        # =====================================

        improvement_note = ""

        if state.feedback:

            improvement_note = f"""
Previous answer failed review.

Reviewer feedback:
{state.feedback}
"""

        # =====================================
        # STEP 4: PLAN TO TEXT
        # =====================================

        steps_text = "\n".join(
            [
                f"{step['id']}. "
                f"{step['action']} - "
                f"{step['description']}"
                for step in plan["steps"]
            ]
        )

        goal_lower = user_goal.lower()

        # =====================================
        # STEP 5: FORMAT RULES
        # =====================================

        format_rules = """
- Never add introductions
- Never add conclusions
- Output ONLY the final answer
"""

        # sentence format
        if "sentence" in goal_lower:

            format_rules += """
- Output EXACTLY the requested number of sentences
- Output ONLY plain sentences
- Do NOT use numbering
- Do NOT use bullet points
"""

        # point format
        elif "point" in goal_lower or "bullet" in goal_lower:

            format_rules += """
- Output EXACTLY the requested number of numbered points
- Use ONLY this format:
  1.
  2.
  3.
- Never use "-" bullets
- Never use nested bullets
"""

        # =====================================
        # STEP 6: FINAL LLM EXECUTION
        # =====================================

        prompt = f"""
{improvement_note}

You are an execution agent.

User goal:
{user_goal}

Plan:
{steps_text}

Generate the FINAL ANSWER that EXACTLY matches the requested format.

STRICT FORMAT RULES:
{format_rules}
"""

        state.final_answer = (
            self.llm.generate(prompt).strip()
        )