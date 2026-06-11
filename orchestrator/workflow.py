from agents.planner import PlannerAgent
from agents.executor import ExecutorAgent
from agents.reviewer import ReviewerAgent
from orchestrator.state import WorkflowState


def run_workflow(user_input: str) -> str:
    planner = PlannerAgent()
    executor = ExecutorAgent()
    reviewer = ReviewerAgent()
    state = WorkflowState()

    plan = planner.plan(user_input)

    while state.retry_count <= state.max_retries:

        print(f"\n--- Attempt {state.retry_count + 1} ---")

        # reset state for fresh execution
        state.research_notes = []
        state.key_points = []
        state.final_answer = None

        # run execution
        executor.execute(plan, state, user_input)

        if not state.final_answer:
            return "No final answer produced."

        review = reviewer.review(user_input, state.final_answer)

        if review["approved"]:
            print("✅ Approved by reviewer")
            return state.final_answer

        # ❌ Not approved → retry
        print("❌ Rejected:", review["feedback"])

        state.feedback = review["feedback"]
        state.retry_count += 1

    return "Failed after retries."