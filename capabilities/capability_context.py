class CapabilityContext:

    def __init__(

        self,

        state,

        tool_registry=None,

        capability_manager=None

    ):

        self.state = state

        self.tool_registry = tool_registry

        self.capability_manager = capability_manager

    # --------------------------------------------

    def trace(
        self,
        message
    ):

        self.state.add_trace(message)

    # --------------------------------------------

    def invoke_tool(

        self,

        tool_name,

        **kwargs

    ):

        if self.tool_registry is None:

            raise Exception(
                "Tool Registry not configured."
            )

        tool = self.tool_registry.get_tool(
            tool_name
        )

        if tool is None:

            raise Exception(
                f"Unknown Tool: {tool_name}"
            )

        return tool.execute(**kwargs)

    # --------------------------------------------

    def invoke_capability(

        self,

        capability_name,

        request

    ):

        if self.capability_manager is None:

            raise Exception(
                "Capability Manager not configured."
            )

        return self.capability_manager.execute(

            capability_name,

            request,

            self.state

        )