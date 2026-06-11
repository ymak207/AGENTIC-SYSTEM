from tools.tool_registry import TOOLS


class ToolExecutor:

    def execute(self, tool_name: str, tool_input: str) -> dict:

        # =====================================
        # TOOL VALIDATION
        # =====================================

        if tool_name not in TOOLS:

            return {
                "success": False,
                "error": f"Unknown tool: {tool_name}"
            }

        try:

            tool_function = TOOLS[tool_name]["function"]

            result = tool_function(tool_input)

            if isinstance(result, str):

                error_prefixes = ["Calculation error", "Invalid characters", "Error"]

                if any(
                    result.startswith(prefix)
                    for prefix in error_prefixes
                ):

                    return {
                        "success": False,
                        "tool_name": tool_name,
                        "tool_input": tool_input,
                        "error": result
                    }
                

            return {
                "success": True,
                "tool_name": tool_name,
                "tool_input": tool_input,
                "result": result
            }

        except Exception as e:

            return {
                "success": False,
                "tool_name": tool_name,
                "tool_input": tool_input,
                "error": str(e)
            }