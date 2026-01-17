from agents.planner import PlannerAgent


def run_workflow(user_input: str):
    planner = PlannerAgent()
    plan = planner.plan(user_input)
    return plan
