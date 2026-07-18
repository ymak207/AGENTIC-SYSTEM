from routing.intent_router import IntentRouter
from agents.planner import PlannerAgent


router = IntentRouter()

planner = PlannerAgent()


tests = [

    "Explain Docker",

    "23*44",

    "Explain Docker and calculate 23*44",

    "What is my profession",

    "Latest AWS announcements"

]


for goal in tests:

    print("=" * 80)
    print(goal)
    print("=" * 80)

    routing = router.route(goal)

    print("\nRouting")
    print(routing)

    plan = planner.plan(
        goal,
        routing
    )

    print("\nPlanner")
    print(plan)

    assert "capabilities" in routing

    assert isinstance(
        routing["capabilities"],
        list
    )

    assert "goal" in plan

    assert "steps" in plan

    assert len(plan["steps"]) > 0

print("\nIntent -> Capability -> Planner test passed.")