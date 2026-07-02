from agents.planner import PlannerAgent
from orchestrator.state import WorkflowState

planner = PlannerAgent()

state = WorkflowState()

plan = planner.plan(
    "Calculate 25 * 15",
    state
)

print(plan)

print("\nTRACE")

for item in state.trace:
    print(item)