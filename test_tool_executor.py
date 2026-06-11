from tools.tool_executor import ToolExecutor

executor = ToolExecutor()

result = executor.execute(
    "calculator",
    "25 * 10"
)

print(result)

