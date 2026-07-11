class CapabilityRegistry:

    def __init__(self):

        self.capabilities = {}

    # --------------------------------------------

    def register(
        self,
        capability
    ):

        self.capabilities[
            capability.name
        ] = capability

    # --------------------------------------------

    def get(
        self,
        capability_name
    ):

        return self.capabilities.get(
            capability_name
        )

    # --------------------------------------------

    def list_capabilities(self):

        return list(
            self.capabilities.keys()
        )