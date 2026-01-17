import json
from llm.ollama_llm import OllamaLLM


PLANNER_PROMPT = """
You are a planning agent.

Rules:
- Do NOT execute tasks
- Do NOT use tools
- Do NOT add explanations
- Output ONLY valid JSON
- Break the task into minimal, logical steps

Output format:
{
  "goal": "<original user goal>",
  "steps": [
    { "id": 1, "action": "<action>", "description": "<what to do>" }
  ]
}
"""


class PlannerAgent:
    def __init__(self):
        self.llm = OllamaLLM()

    def plan(self, user_goal: str) -> dict:
        prompt = f"{PLANNER_PROMPT}\nUser goal: {user_goal}"
        response = self.llm.generate(prompt)

        try:
            return json.loads(response)
        except json.JSONDecodeError:
            raise ValueError(f"Planner returned invalid JSON:\n{response}")
