class WorkflowState:
    """
    Shared mutable state across planner and executor steps.
    """

    def __init__(self):

        
        self.final_answer: str | None = None

        self.retry_count: int = 0
        self.max_retries: int = 2
        self.feedback: str | None = None
