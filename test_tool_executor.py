from agents.planner import PlannerAgent
from agents.executor import ExecutorAgent
from orchestrator.state import WorkflowState

planner = PlannerAgent()
executor = ExecutorAgent()

state = WorkflowState()

goal = "What is 25 * 15?"

plan = planner.plan(
    goal,
    state
)

executor.execute(
    plan,
    state,
    goal
)

print("\nFINAL ANSWER\n")
print(state.final_answer)

print("\nTRACE\n")

for item in state.trace:
    print(item)

print("\nTOOL CALLS\n")
print(state.tool_calls)