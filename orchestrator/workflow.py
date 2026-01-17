from agents.planner import PlannerAgent
from agents.executor import ExecutorAgent

def run_workflow(user_input: str) -> str:
    planner = PlannerAgent()
    executor = ExecutorAgent()

    plan = planner.plan(user_input)

    context = ""
    outputs = []

    for step in plan["steps"]:
        result = executor.execute_step(step, context)
        outputs.append(result)
        context += "\n" + result

    return "\n\n".join(outputs)
