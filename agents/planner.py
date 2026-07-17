import json
import re

from llm.ollama_llm import OllamaLLM


PLANNER_PROMPT = """
You are an Enterprise AI Planning Agent.

Your ONLY responsibility is to create an execution plan.

Routing has ALREADY been decided.

DO NOT

- answer the user
- choose knowledge sources
- choose tools
- modify routing
- execute any step
- calculate results
- browse the web
- retrieve memory
- retrieve RAG
- include URLs
- include code

Return ONLY VALID JSON.

Every object inside steps must contain exactly:

id
action
description

The JSON MUST be directly parsable using Python json.loads().

IMPORTANT

Before returning your answer, mentally verify that every string is valid JSON.

FINAL SELF CHECK

Before returning your response, pretend it will immediately be executed as:

json.loads(your_output)

If parsing would fail for any reason,

fix the JSON before returning it.

Do not return JSON that would fail parsing.

The output will be parsed directly using Python json.loads().

Quotation Rules

Avoid quotation marks inside string values whenever possible.

Preferred

"description":"Search the Docker documentation."

Preferred

"description":"Open the Announcements section."

Instead of

"description":"Open the "Announcements" section."

rewrite it as

"description":"Open the Announcements section."

Only use quotation marks when absolutely necessary.

If quotation marks are required,
escape them using \".

Never place unescaped double quotes inside JSON string values.

Correct

{
    "goal":"Determine user's profession"
}

Correct

{
    "goal":"Determine user\"s profession"
}

Wrong

{
    "goal":"Determine user"s profession"
}

If any string contains a double quote ("),
it MUST be escaped as \".

Never output invalid JSON.

JSON Rules

- Use ONLY double quotes.
- NEVER use single quotes.
- Escape any double quotes inside strings using \\"
- Never wrap JSON inside markdown.
- Never write explanations.
- Never add text before or after JSON.
- Never include comments.
- Never include trailing commas.
- Every string must be valid JSON.
- If a sentence requires quotation marks inside a string,
escape them using \".
Example
"description":"Type \"hello\" into the console."

The planner creates ONLY execution steps.

Do not mention implementation names like:

- RAG
- Memory
- Web
- Calculator

Describe the task instead.

Good

Retrieve Docker information

Bad

Retrieve Docker from RAG

Steps describe WHAT should happen.

Every step MUST contain:

- id
- action
- description

description must never be empty.

Never omit required fields.

Steps NEVER contain:

- results
- answers
- retrieved content
- URLs
- example outputs
- calculated values

Step Writing Rules

- Describe the task, not the exact user input.
- Do not include URLs.
- Do not include quoted phrases unless properly escaped.
- Keep action concise.
- Keep description concise.
- Prefer generic task descriptions over literal examples.

The routing below is FINAL.

Never create steps that require knowledge sources or tools that are NOT present in the provided routing.

If knowledge_sources is empty,
do not create retrieval steps.

If tools is empty,
do not create tool execution steps.

Every step must be achievable using ONLY the provided routing.

You MUST copy it exactly.

Every step MUST contain ALL of the following fields.

- id
- action
- description

The description field is mandatory.

Never omit it.

Never leave it empty.

If you cannot think of a better description,
repeat the action as the description.

Output format

{
    "goal":"...",
    "knowledge_sources":[],
    "tools":[],
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

    def _normalize_json(self, text: str) -> str:
        """
        Fix common LLM JSON mistakes before json.loads().
        """
    
        
    
        # Python literals -> JSON literals
        text = text.replace("True", "true")
        text = text.replace("False", "false")
        text = text.replace("None", "null")
    
        return text
    
    def _sanitize_json(self, text):

        return self._normalize_json(text)

    def _extract_json(self, text: str) -> str:
        """
        Extract JSON from LLM output.
    
        Handles:
        - ```json ... ```
        - Here is the corrected JSON...
        - Extra explanations
        """
    
        text = text.strip()
    
        # Look for fenced JSON first
        match = re.search(
            r"```(?:json)?\s*(.*?)```",
            text,
            flags=re.DOTALL | re.IGNORECASE
        )
    
        if match:
            return match.group(1).strip()
    
        # Otherwise find first JSON object
        start = text.find("{")
        end = text.rfind("}")
    
        if start == -1 or end == -1:
            raise ValueError("No JSON found.")
    
        return text[start:end + 1]

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

            for field in (
                "id",
                "action",
                "description"
            ):
        
                if field not in step:
                    raise ValueError(
                        f"Step missing '{field}'"
                    )
    
            if not isinstance(step["id"], int):
                raise ValueError("step id must be integer")
        
            if step["id"] <= 0:
                raise ValueError("step id must be positive")
        
            if not isinstance(step["action"], str):
                raise ValueError("action must be string")
        
            if not step["action"].strip():
                raise ValueError("action cannot be empty")
        
            if not isinstance(step["description"], str):
                raise ValueError("description must be string")
        
            
    
        # -------------------------------------------------
    def _clean_plan(self, plan, routing):

        plan["knowledge_sources"] = routing["knowledge_sources"]
        plan["tools"] = routing["tools"]
    
        allowed = {"id", "action", "description"}
    
        for step in plan["steps"]:
    
            # Ensure description always exists
            step.setdefault(
                "description",
                step.get("action", "")
            )
    
            if isinstance(step["description"], str):
                step["description"] = step["description"].strip()
    
            if not step["description"]:
                step["description"] = step.get(
                    "action",
                    ""
                )
    
            # Remove unexpected fields
            for key in list(step.keys()):
                if key not in allowed:
                    del step[key]
    
        return plan
    
    def _repair_plan(
    self,
    user_goal,
    broken_response,
    state=None
):

        repair_prompt = f"""
The Planner produced invalid output.

Your task is to repair it.

DO NOT change the meaning.

DO NOT rewrite the plan.

ONLY repair what caused the parser failure.

User Goal

{user_goal}

Broken Planner Output

{broken_response}

Repair Rules

Repair the planner output into valid JSON.

Do NOT change the execution plan.

Do NOT improve the plan.

Do NOT rewrite actions.

Do NOT rewrite descriptions.

Do NOT infer missing information.

Do NOT add new fields.

Preserve the original schema exactly.

Only repair structural problems.

Examples

- invalid JSON
- escaping errors
- missing commas
- trailing commas
- invalid brackets
- incorrect field types

Do not rewrite the execution plan.

Do not improve wording.

Do not invent new actions.

Do not invent new descriptions.

Do not add new steps.

Preserve the original content whenever possible.

Allowed top-level fields

goal
knowledge_sources
tools
steps

Allowed step fields

id
action
description

Return ONLY valid JSON."""

        if state:

            state.metrics["llm_calls"] += 1
        if state:
            state.metrics["planner_repairs"] += 1

        repaired = self.llm.generate(repair_prompt).strip()
        
        json_text = self._extract_json(repaired)

        json_text = self._sanitize_json(json_text)

        print("\n===== Repair JSON =====")
        print(json_text)
        print("=======================\n")
        
        return json.loads(json_text)

    # -------------------------------------------------

    def plan(

        self,
    
        user_goal,
    
        routing,
    
        state=None
    
    ):

        if state:

            state.add_trace(

                "Planner Started"

            )

        

        prompt = f"""
{PLANNER_PROMPT}

User Goal

{user_goal}

Knowledge Sources

{routing["knowledge_sources"]}

Tools

{routing["tools"]}

Create ONLY execution steps.

Return the SAME knowledge_sources and tools exactly as provided.
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

            json_text = self._extract_json(response)

            json_text = self._sanitize_json(json_text) 

            print("\n===== Planner JSON =====")
            print(json_text)
            print("========================\n")
                        
            plan = json.loads(json_text)

            plan = self._clean_plan(plan, routing)
            
            self._validate_plan(plan)

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

            plan = self._clean_plan(plan, routing)

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