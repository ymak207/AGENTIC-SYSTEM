from capabilities.capability_manager import (
    CapabilityManager
)

from capabilities.compute.compute_capability import (
    ComputeCapability
)


class DummyState:

    def __init__(self):

        self.trace = []

    def add_trace(
        self,
        message
    ):
        self.trace.append(message)


manager = CapabilityManager()

manager.register(
    ComputeCapability()
)

state = DummyState()

result = manager.execute(
    "compute",
    {
        "expression": "125*84"
    },
    state
)

print(result)

print()

for item in state.trace:
    print(item)