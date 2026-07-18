class ComputeExecutor:

    def execute(
        self,
        step,
        state,
        user_goal
    ):

        state.add_trace(
            f"Compute capability executed: {step['action']}"
        )