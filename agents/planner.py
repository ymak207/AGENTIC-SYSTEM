import json

from llm.ollama_llm import OllamaLLM


PLANNER_PROMPT = """
You are an Enterprise AI Planning Agent.

Return ONLY valid JSON.

Your responsibilities are:

1. Decide which knowledge sources are required.
2. Decide which tools are required.
3. Produce the minimum execution steps.
4. Never retrieve unnecessary information.
5. NEVER execute calculations.
6. NEVER answer the user's question.
7. ONLY create a plan.

------------------------------------------------

AVAILABLE KNOWLEDGE SOURCES

memory
- User profile
- Previous conversations
- Personal facts
- Stored preferences

rag
- Uploaded PDFs
- Company documentation
- Policies
- Manuals
- Knowledge Base

web
- Latest information
- News
- Current events
- Live internet information

------------------------------------------------

AVAILABLE TOOLS

calculator

------------------------------------------------

KNOWLEDGE SELECTION RULES

User profile
→ memory

Uploaded documents
→ rag

Company policies
→ rag

Manuals
→ rag

Latest information
→ web

Today's information
→ web

Current information
→ web

Recent news
→ web

Mathematics or calculations
→ calculator
AND use an empty knowledge_sources list.

Company documents + latest information
→ rag + web

User profile + company documents
→ memory + rag

User profile + latest information
→ memory + web

------------------------------------------------

IMPORTANT RULES

If uploaded documents can answer the question,
DO NOT use web.

Use web ONLY when the user explicitly requests:
- latest
- current
- today
- recent
- news
- live
- internet

Never mix company documents with web unless
the user explicitly asks to compare or combine.

Allowed knowledge_sources are ONLY

memory
rag
web

Allowed tools are ONLY

calculator

Do NOT invent new knowledge sources.

Do NOT invent new tools.

Do NOT calculate answers.

The executor performs calculations.

------------------------------------------------

Return EXACTLY

{
    "goal":"...",

    "knowledge_sources":[
        "memory"
    ],

    "tools":[
        "calculator"
    ],

    "steps":[
        {
            "id":1,
            "action":"...",
            "description":"..."
        }
    ]
}
"""


class PlannerAgent:

    ALLOWED_KNOWLEDGE = {

        "memory",

        "rag",

        "web"

    }

    ALLOWED_TOOLS = {

        "calculator"

    }

    def __init__(self):

        self.llm = OllamaLLM()

    # -------------------------------------------------

    def _validate_plan(
        self,
        plan
    ):

        required = [

            "goal",

            "knowledge_sources",

            "tools",

            "steps"

        ]

        for field in required:

            if field not in plan:

                raise ValueError(

                    f"Planner missing '{field}'"

                )

        if not isinstance(
            plan["knowledge_sources"],
            list
        ):

            raise ValueError(
                "knowledge_sources must be a list"
            )

        if not isinstance(
            plan["tools"],
            list
        ):

            raise ValueError(
                "tools must be a list"
            )

        if not isinstance(
            plan["steps"],
            list
        ):

            raise ValueError(
                "steps must be a list"
            )

        if len(plan["steps"]) == 0:

            raise ValueError(
                "Planner produced zero steps."
            )

        # -----------------------------
        # Validate Knowledge Sources
        # -----------------------------

        for source in plan["knowledge_sources"]:

            if source not in self.ALLOWED_KNOWLEDGE:

                raise ValueError(

                    f"Invalid knowledge source '{source}'"

                )

        # -----------------------------
        # Validate Tools
        # -----------------------------

        for tool in plan["tools"]:

            if tool not in self.ALLOWED_TOOLS:

                raise ValueError(

                    f"Invalid tool '{tool}'"

                )

        # -----------------------------
        # Validate Steps
        # -----------------------------

        for step in plan["steps"]:

            for field in [

                "id",

                "action",

                "description"

            ]:

                if field not in step:

                    raise ValueError(

                        f"Step missing '{field}'"

                    )

    # -------------------------------------------------

    def _repair_plan(

        self,

        user_goal,

        broken_response,

        state=None

    ):

        repair_prompt = f"""
The previous JSON is INVALID because of formatting.

Your job is ONLY to repair the JSON.

DO NOT

- change the goal
- change the meaning
- invent knowledge sources
- invent tools
- invent new steps

Allowed knowledge_sources

memory
rag
web

Allowed tools

calculator

User Goal

{user_goal}

Broken JSON

{broken_response}

Return ONLY corrected JSON.
"""

        if state:

            state.metrics["llm_calls"] += 1

        repaired = self.llm.generate(

            repair_prompt

        ).strip()

        return json.loads(repaired)

    # -------------------------------------------------

    def plan(

        self,

        user_goal,

        state=None

    ):

        if state:

            state.add_trace(

                "Planner Started"

            )

        memory_context = ""

        if (

            state

            and

            state.knowledge["memory"]

        ):

            memory_context = (

                "\nKnown User Memory\n"

                + "\n".join(

                    state.knowledge["memory"]

                )

            )

        prompt = f"""

{PLANNER_PROMPT}

{memory_context}

User Goal

{user_goal}

"""

        if state:

            state.metrics["llm_calls"] += 1

        response = self.llm.generate(

            prompt

        ).strip()

        if state:

            state.add_trace(

                "Planner Response Received"

            )

        try:

            plan = json.loads(

                response

            )

            self._validate_plan(

                plan

            )

        except Exception as ex:

            if state:

                state.add_trace(

                    f"Planner Repair Started ({str(ex)})"

                )

            plan = self._repair_plan(

                user_goal,

                response,

                state

            )

            self._validate_plan(

                plan

            )

            if state:

                state.add_trace(

                    "Planner Repair Completed"

                )

        if state:

            state.plan = plan

            state.add_trace(

                "Planner Completed"

            )

        return plan