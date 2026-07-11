from agents.planner import PlannerAgent

from orchestrator.state import WorkflowState

from knowledge.knowledge_manager import KnowledgeManager


planner = PlannerAgent()

knowledge = KnowledgeManager()

state = WorkflowState()


queries = [

    "What is my profession?",

    "Explain AWS Well Architected Framework.",

    "Latest AWS announcements",

    "125 * 84"

]


for query in queries:

    print()

    print("=" * 80)

    print(query)

    print("=" * 80)

    plan = planner.plan(

        query,

        state

    )

    print()

    print("Planner Selected")
    
    print("----------------")
    
    print("Knowledge :", plan["knowledge_sources"])
    
    print("Tools     :", plan["tools"])

    knowledge.retrieve(

        query,

        plan,

        state

    )

    print()

    print("Memory Loaded :", len(state.knowledge["memory"]))

    print("RAG Loaded    :", len(state.knowledge["rag"]))

    print("Web Loaded    :", len(state.knowledge["web"]))

    print()

    state.knowledge = {

        "memory": [],

        "rag": [],

        "web": []

    }