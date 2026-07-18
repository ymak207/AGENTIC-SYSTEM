from agents.executor import ExecutorAgent
from orchestrator.state import WorkflowState

executor = ExecutorAgent()

state = WorkflowState()

plan = {
    "goal": "Explain Docker and calculate 23*44",
    "steps": [
        {
            "id": 1,
            "capability": "knowledge",
            "action": "Retrieve Docker information",
            "description": "Gather Docker details"
        },
        {
            "id": 2,
            "capability": "compute",
            "action": "Perform multiplication",
            "description": "Calculate 23*44"
        }
    ]
}

executor.execute(
    plan=plan,
    state=state,
    user_goal="Explain Docker and calculate 23*44"
)

print("\nTrace\n")

for item in state.trace:
    print(item)

print("\nExecutor capability flow test passed.")