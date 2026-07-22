import json
import re

from llm.ollama_llm import OllamaLLM

PLANNER_PROMPT = """
You are an Enterprise AI Planning Agent.

Your ONLY responsibility is to create a capability-level execution plan.

You DO NOT execute tasks.
You DO NOT answer the user.
You ONLY decide which capabilities are required.

Routing has already been decided.

Never:

- answer the user
- calculate results
- browse the web
- retrieve memory
- retrieve documents
- select tools
- choose providers
- modify routing
- execute any capability
- include URLs
- include code
- include markdown

----------------------------------------------------
Planning Rules
----------------------------------------------------

The planner works ONLY at capability level.

Each capability may appear ONLY ONCE.

If multiple activities belong to the same capability,
merge them into ONE step.

Never split one capability into multiple steps.

Example

GOOD

Knowledge
Compute

BAD

Knowledge
Knowledge
Compute

BAD

Knowledge
Knowledge
Knowledge

The Executor is responsible for everything inside a capability.

The Planner only decides:

- which capabilities are needed
- execution order

----------------------------------------------------
Output Schema
----------------------------------------------------

Return ONLY valid JSON.

{
    "goal":"...",
    "steps":[
        {
            "id":1,
            "capability":"knowledge",
            "action":"...",
            "description":"..."
        }
    ]
}

Each step MUST contain

- id
- capability
- action
- description

Description must never be empty.

----------------------------------------------------
JSON Rules
----------------------------------------------------

Return ONLY JSON.

No markdown.

No explanations.

No comments.

No trailing commas.

Use only double quotes.

Escape embedded quotes using \\"

Output must be directly parsable using Python json.loads().

----------------------------------------------------
Writing Rules
----------------------------------------------------

Actions should be concise.

Descriptions should be generic.

Describe WHAT should happen.

Never describe HOW.

Never mention:

- Memory
- RAG
- Web
- Calculator
- Tools
- Providers

Good

Retrieve Docker information

Bad

Retrieve Docker using RAG

----------------------------------------------------
Goal Preservation
----------------------------------------------------

Preserve the supplied User Goal exactly.

Do not rewrite it.

Do not infer a different task.

----------------------------------------------------
Final Self Check
----------------------------------------------------

Before returning:

1. Every capability appears only once.
2. Every step has id, capability, action and description.
3. JSON parses with json.loads().
4. No markdown.
5. No explanations.
"""

class PlannerAgent:

    

    def __init__(self):

        self.llm = OllamaLLM()

        self.allowed_capabilities = [
            "knowledge",
            "compute"
        ]

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
                "steps"
            ]
        
        if not isinstance(plan["goal"], str):
            raise ValueError("goal must be string")
        
        if not plan["goal"].strip():
            raise ValueError("goal cannot be empty")

        for field in required:

            if field not in plan:

                raise ValueError(

                    f"Planner missing '{field}'"

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
        # Validate Steps
        # -----------------------------

        for step in plan["steps"]:

            for field in (
                "id",
                "capability",
                "action",
                "description"
            ):
        
                if field not in step:
                    raise ValueError(
                        f"Step missing '{field}'"
                    )
                
            allowed_capabilities = {
                "knowledge",
                "compute"
            }.intersection(set(self.allowed_capabilities))
            
            if step["capability"] not in allowed_capabilities:
                raise ValueError(
                    f"Invalid capability {step['capability']}"
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
        
        # -----------------------------
        # Duplicate capability check
        # -----------------------------
        
        capabilities = [
            step["capability"]
            for step in plan["steps"]
        ]
        
        if len(capabilities) != len(set(capabilities)):
            raise ValueError(
                "Planner produced duplicate capability steps."
            )
        
        ids = [step["id"] for step in plan["steps"]]
        
        if len(ids) != len(set(ids)):
            raise ValueError("Duplicate step ids.")
                

        
        
            
    

    def _repair_plan(
    self,
    user_goal,
    broken_response,
    state=None
):

        repair_prompt = f"""
The Planner produced invalid output.

Repair the planner output.

User Goal

{user_goal}

Broken Planner Output

{broken_response}

Repair Rules

Repair ONLY the planner output.

Do not answer the user.

Do not execute anything.

Preserve the original goal.

Preserve the original execution intent.

Return ONLY valid JSON.

Required schema

goal

steps[]

Each step must contain

- id
- capability
- action
- description

Business Rules

- Each capability may appear ONLY ONCE.
- Merge duplicate capability steps into a single step.
- Never invent new capabilities.
- Never remove required capabilities.
- Preserve execution order whenever possible.
- Keep actions concise.
- Keep descriptions concise.
- Description must never be empty.
- Do not include tools.
- Do not include providers.
- Do not include URLs.
- Do not include results.
- Do not include markdown.
- Return ONLY parsable JSON.

If duplicate capability steps exist,
merge them into one generic capability step.

The repaired output must parse successfully using Python json.loads().
"""

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

User Goal:
{user_goal}

Available Capabilities:
{json.dumps(routing["capabilities"])}

Return ONLY valid JSON.
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