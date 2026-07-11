from agents.planner import PlannerAgent

from orchestrator.state import WorkflowState


planner = PlannerAgent()

state = WorkflowState()

# -------------------------------------------------------
# Simulate previously retrieved memory
# -------------------------------------------------------

state.knowledge["memory"] = [

    "User works as WebMethods Developer.",

    "User is learning Agentic AI."

]

# -------------------------------------------------------
# Test Queries
# -------------------------------------------------------

queries = [

    "What is my profession?",

    "Explain AWS Well Architected Framework from uploaded documents.",

    "What are the latest AWS announcements?",

    "Compare latest AWS announcements with my uploaded AWS document.",

    "125 * 84",

    "Summarize my uploaded AWS document.",

    "Compare my uploaded company policy with today's AWS announcement."

]

# -------------------------------------------------------

for query in queries:

    print()

    print("=" * 80)

    print("QUERY")

    print("=" * 80)

    print(query)

    print()

    plan = planner.plan(

        query,

        state

    )

    print("=" * 80)

    print("PLANNER OUTPUT")

    print("=" * 80)

    print()

    print("Goal")

    print("-----")

    print(plan["goal"])

    print()

    print("Knowledge Sources")

    print("-----------------")

    print(plan["knowledge_sources"])

    print()

    print("Tools")

    print("-----")

    print(plan["tools"])

    print()

    print("Steps")

    print("-----")

    for step in plan["steps"]:

        print(

            f'{step["id"]}. '

            f'{step["action"]}'

        )

        print(

            f'   {step["description"]}'

        )

        print()