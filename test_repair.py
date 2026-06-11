from agents.planner import PlannerAgent

planner = PlannerAgent()

broken_plan = """
{
  "goal": "Calculate 25 * 10",
  "steps": [
    {
      "id": 1,
      "action": "multiply"
    }
  ]
}
"""

repaired = planner._repair_plan(
    user_goal="Calculate 25 * 10",
    broken_response=broken_plan
)

print(repaired)