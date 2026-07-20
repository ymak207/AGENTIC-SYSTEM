import time

from agents.planner import PlannerAgent
from agents.executor import ExecutorAgent
from agents.reviewer import ReviewerAgent
from routing.intent_router import IntentRouter

from orchestrator.state import WorkflowState
from orchestrator.workflow_status import WorkflowStatus





def run_workflow(user_input: str) -> WorkflowState:

    workflow_start = time.time()

    planner = PlannerAgent()
    intent_router = IntentRouter()
    executor = ExecutorAgent()
    reviewer = ReviewerAgent()

    state = WorkflowState()

    # ==========================================
    # Live Workflow Status
    # ==========================================

    status = WorkflowStatus()

    state.workflow_status = status.to_list()

    state.add_trace(
        "Workflow Started"
    )

    # ==========================================
    # PLANNER
    # ==========================================

    status.start("planner")

    state.workflow_status = status.to_list()

    planner_start = time.time()

    routing = intent_router.route(
    user_input
    )
    
    state.add_trace(
        "Intent Routing Completed"
    )
    
    plan = planner.plan(
        user_input,
        routing,
        state
    )

    planner_end = time.time()

    state.metrics["planner_seconds"] = round(
        planner_end - planner_start,
        2
    )

    status.complete("planner")

    state.workflow_status = status.to_list()

    

    # ==========================================
    # EXECUTION LOOP
    # ==========================================

    while state.retry_count <= state.max_retries:

        attempt_number = state.retry_count + 1

        print(
            f"\n--- Attempt {attempt_number} ---"
        )

        state.add_trace(
            f"Attempt {attempt_number} Started"
        )

        state.final_answer = None

        # ======================================
        # EXECUTOR
        # ======================================

        status.start("executor")

        state.workflow_status = status.to_list()

        executor_start = time.time()

        executor.execute(
            plan,
            state,
            user_input
        )

        executor_end = time.time()

        state.metrics["executor_seconds"] += round(
            executor_end - executor_start,
            2
        )

        status.complete("executor")

        state.workflow_status = status.to_list()

        # ======================================
        # EXECUTOR FAILED
        # ======================================

        if not state.final_answer:

            state.add_trace(
                "Workflow Failed: No Final Answer"
            )

            workflow_end = time.time()

            state.metrics["workflow_seconds"] = round(
                workflow_end - workflow_start,
                2
            )

            return state

        # ======================================
        # REVIEWER
        # ======================================

        status.start("reviewer")

        state.workflow_status = status.to_list()

        reviewer_start = time.time()

        review = reviewer.review(
            user_input,
            state.final_answer,
            state
        )

        reviewer_end = time.time()

        state.metrics["reviewer_seconds"] += round(
            reviewer_end - reviewer_start,
            2
        )

        status.complete("reviewer")

        state.workflow_status = status.to_list()

        # ======================================
        # APPROVED
        # ======================================

        if review["approved"]:

            saved_count = executor.knowledge_executor.manager.save_memory(
    user_input
)

            state.metrics[
                "memories_saved"
            ] += saved_count

            state.add_trace(
                f"Memory Saved ({saved_count})"
            )

            state.add_trace(
                "Workflow Approved"
            )

            status.finish()

            state.workflow_status = status.to_list()

            state.add_trace(
                "Workflow Completed"
            )

            workflow_end = time.time()

            state.metrics["workflow_seconds"] = round(
                workflow_end - workflow_start,
                2
            )

            print(
                "✅ Approved by reviewer"
            )

            return state

        # ======================================
        # REJECTED
        # ======================================

        state.add_trace(
            f"Workflow Rejected: {review['feedback']}"
        )

        print(
            "❌ Rejected:",
            review["feedback"]
        )

        state.feedback = review["feedback"]

        state.retry_count += 1

        state.add_trace(
            f"Retry Count = {state.retry_count}"
        )

    # ==========================================
    # FAILED AFTER RETRIES
    # ==========================================

    state.add_trace(
        "Workflow Failed After Retries"
    )

    workflow_end = time.time()

    state.metrics["workflow_seconds"] = round(
        workflow_end - workflow_start,
        2
    )

    return state