from datetime import datetime   # <-- NEW


class WorkflowState:
    """
    Shared mutable state across planner and executor steps.
    """

    def __init__(self):

        self.final_answer: str | None = None

        self.retry_count: int = 0
        self.max_retries: int = 2
        self.feedback: str | None = None

        # ==================================================
        # OBSERVABILITY - NEW
        # ==================================================

        # Stores planner output
        self.plan: dict | None = None

        # Timeline of events
        self.trace: list = []

        # Tool execution history
        self.tool_calls: list = []

        self.knowledge = {

                "memory": [],
            
                "rag": [],
            
                "web": []
            
            }
        
        self.compute_results = []
        
        self.workflow_status = []

        # Timing and metrics
        self.metrics = {
    "planner_seconds": 0,
    "executor_seconds": 0,
    "reviewer_seconds": 0,
    "workflow_seconds": 0,
    "llm_calls": 0,
    "memories_loaded": 0,
    "memories_saved": 0,
    "planner_repairs": 0
}
    # ==================================================
    # OBSERVABILITY - NEW
    # ==================================================

    def add_trace(self, event: str):
        """
        Add timestamped event to execution trace.
        """

        self.trace.append(
            {
                "timestamp": datetime.now().strftime("%H:%M:%S"),
                "event": event,
            }
        )