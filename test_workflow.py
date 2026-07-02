from orchestrator.workflow import (
    run_workflow
)

state = run_workflow(

    "What are the six pillars of the AWS Well-Architected Framework?"

)

print()

print("MEMORY")

print("-" * 50)

print(state.knowledge["memory"])

print()

print("RAG")

print("-" * 50)

print(len(state.knowledge["rag"]))

print()

print("ANSWER")

print("-" * 50)

print(state.final_answer)

print()

print("TRACE")

print("-" * 50)

for item in state.trace:

    print(

        item["event"]

    )