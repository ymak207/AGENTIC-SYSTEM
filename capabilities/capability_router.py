class CapabilityRouter:

    def route(
        self,
        plan
    ):

        capabilities = []

        knowledge = plan.get(
            "knowledge_sources",
            []
        )

        tools = plan.get(
            "tools",
            []
        )

        if knowledge:

            capabilities.append(
                "knowledge"
            )

        if "calculator" in tools:

            capabilities.append(
                "compute"
            )

        return capabilities