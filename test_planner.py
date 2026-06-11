from agents.planner import PlannerAgent


planner = PlannerAgent()

planner._validate_plan(
    {
        "goal": "test",
        "steps": [
            {
                "id": 1,
                "action": "multiply",
                "description": "Multiply values"
            }
        ]
    }
)