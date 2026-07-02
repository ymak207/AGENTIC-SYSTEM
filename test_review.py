from agents.reviewer import ReviewerAgent
from orchestrator.state import WorkflowState

reviewer = ReviewerAgent()

state = WorkflowState()

result = reviewer.review(
    user_goal="Give me 3 numbered points about AWS",
    answer="""
1. AWS provides cloud services.
2. AWS supports scalability.
3. AWS offers managed databases.
""",
    state=state
)

print(result)

print("\nTRACE\n")

for item in state.trace:
    print(item)