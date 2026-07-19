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

for query in tests:

    print("=" * 80)
    print(query)
    print("=" * 80)

    routing = router.route(
        query
    )

    print("\nRouting\n")
    print(routing)

    plan = planner.plan(
        user_goal=query,
        routing=routing
    )

    print("\nPlanner\n")
    print(plan)

    assert "capabilities" in routing

    assert isinstance(
        routing["capabilities"],
        list
    )

    assert len(
        routing["capabilities"]
    ) > 0

    assert "goal" in plan

    assert "steps" in plan

    assert len(
        plan["steps"]
    ) > 0

    for step in plan["steps"]:

        assert step["capability"] in routing["capabilities"]

print("\nIntent -> Capability -> Planner test passed.")