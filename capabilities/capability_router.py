class CapabilityRouter:

    def route(
        self,
        intent
    ):

        capabilities = []

        if intent.get("knowledge_required"):

            capabilities.append(
                "knowledge"
            )

        if intent.get("compute_required"):

            capabilities.append(
                "compute"
            )

        return capabilities