from memory.memory_agent import (
    MemoryAgent
)

memory = MemoryAgent()

results = (
    memory.get_relevant_memory(
        "Which certification should I start with?"
    )
)

print()

print("RESULTS")
print("-" * 50)

for item in results:

    print(item)