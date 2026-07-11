from capabilities.capability_context import (
    CapabilityContext
)

from capabilities.capability_registry import (
    CapabilityRegistry
)


class CapabilityManager:

    def __init__(

        self,

        tool_registry=None

    ):

        self.registry = CapabilityRegistry()

        self.tool_registry = tool_registry

    # --------------------------------------------

    def register(

        self,

        capability

    ):

        self.registry.register(
            capability
        )

    # --------------------------------------------

    def execute(

        self,

        capability_name,

        request,

        state

    ):

        capability = self.registry.get(
            capability_name
        )

        if capability is None:

            raise Exception(

                f"Capability '{capability_name}' not found."

            )

        context = CapabilityContext(

            state,

            tool_registry=self.tool_registry,

            capability_manager=self

        )

        state.add_trace(

            f"Capability Started ({capability_name})"

        )

        result = capability.execute(

            request,

            context

        )

        state.add_trace(

            f"Capability Finished ({capability_name})"

        )

        return result