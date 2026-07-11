from capabilities.base_capability import (
    BaseCapability
)

from tools.calculator import (
    calculate
)


class ComputeCapability(BaseCapability):

    @property
    def name(self):
        return "compute"

    def execute(
        self,
        request,
        context
    ):

        context.trace(
            "Compute Capability Executed"
        )

        expression = request.get(
            "expression",
            ""
        )

        result = calculate(
            expression
        )

        return {
            "expression": expression,
            "result": result
        }