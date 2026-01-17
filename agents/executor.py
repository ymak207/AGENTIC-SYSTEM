from llm.ollama_llm import OllamaLLM

class ExecutorAgent:
    def __init__(self):
        self.llm = OllamaLLM()

    def execute_step(self, step: dict, context: str = "") -> str:
        prompt = f"""
You are an execution agent.

Execute ONLY the following step.
Do not plan.
Do not add steps.

Step:
{step['action']}

Context:
{context}

Execution Output:
"""
        return self.llm.generate(prompt).strip()
