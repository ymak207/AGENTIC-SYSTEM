from routing.intent_router import IntentRouter
from agents.planner import PlannerAgent
from orchestrator.state import WorkflowState

router = IntentRouter()
planner = PlannerAgent()

queries = [
    "Explain Docker",
    "Latest AWS announcements",
    "What is my profession",
    "125*84",
    "What is 45 + 78?",
    "Explain Docker and calculate 23*44"
]

for query in queries:

    print("\n" + "=" * 80)
    print(query)
    print("=" * 80)

    routing = router.route(query)

    print("\nRouting")
    print(routing)

    state = WorkflowState()

    plan = planner.plan(
        query,
        routing,
        state
    )

   

    print("\nPlanner Output")
    print(plan)



    print("\nTrace")
    for item in state.trace:
        print(item)