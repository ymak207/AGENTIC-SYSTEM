from memory.memory_agent import MemoryAgent

memory = MemoryAgent()

memory.save_fact(
    "I am learning AWS"
)

memory.save_fact(
    "I work as a WebMethods developer"
)

memory.save_fact(
    "I like cloud computing"
)

print("Saved")