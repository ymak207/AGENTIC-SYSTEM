from llm.ollama_llm import OllamaLLM

from tools.router import ToolRouter
from tools.tool_executor import ToolExecutor


class ExecutorAgent:

    def __init__(self):

        self.llm = OllamaLLM()

        self.router = ToolRouter()

        self.tool_executor = ToolExecutor()

    def execute(self, plan: dict, state, user_goal: str):

        # =====================================
        # OBSERVABILITY
        # =====================================

        state.add_trace(
            "Executor Started"
        )

        # =====================================
        # STEP 1: ROUTE REQUEST
        # =====================================

        tool_decision = self.router.route(user_goal)

        state.add_trace(
            f"Tool Routing Complete "
            f"(use_tool={tool_decision.get('use_tool')})"
        )

        # =====================================
        # STEP 2: EXECUTE TOOL
        # =====================================

        if tool_decision.get("use_tool"):

            tool_name = tool_decision["tool_name"]

            state.add_trace(
                f"Tool Selected: {tool_name}"
            )

            execution_result = self.tool_executor.execute(
                tool_name=tool_name,
                tool_input=tool_decision["tool_input"]
            )

            # =====================================
            # TOOL HISTORY
            # =====================================

            state.tool_calls.append(
                {
                    "tool_name": tool_name,
                    "success": execution_result["success"]
                }
            )

            if execution_result["success"]:

                state.add_trace(
                    f"Tool Success: {tool_name}"
                )

                state.final_answer = (
                    f"Tool Used: "
                    f"{execution_result['tool_name']}\n"
                    f"Result: "
                    f"{execution_result['result']}"
                )

                state.add_trace(
                    "Executor Completed"
                )

                return

            state.add_trace(
                f"Tool Failed: {tool_name}"
            )

            state.final_answer = (
                f"Tool Used: "
                f"{execution_result['tool_name']}\n"
                f"Error: "
                f"{execution_result['error']}"
            )

            state.add_trace(
                "Executor Completed"
            )

            return

        # =====================================
        # STEP 3: RETRY FEEDBACK
        # =====================================

        improvement_note = ""

        if state.feedback:

            state.add_trace(
                "Using Reviewer Feedback"
            )

            improvement_note = f"""
Previous answer failed review.

Reviewer feedback:
{state.feedback}
"""

        # =====================================
        # STEP 4: PLAN TO TEXT
        # =====================================

        steps_text = "\n".join(
            [
                f"{step['id']}. "
                f"{step['action']} - "
                f"{step['description']}"
                for step in plan["steps"]
            ]
        )

        goal_lower = user_goal.lower()

        # =====================================
        # STEP 5: FORMAT RULES
        # =====================================

        format_rules = """
- Never add introductions
- Never add conclusions
- Output ONLY the final answer
"""

        if "sentence" in goal_lower:

            format_rules += """
- Output EXACTLY the requested number of sentences
- Output ONLY plain sentences
- Do NOT use numbering
- Do NOT use bullet points
"""

        elif "point" in goal_lower or "bullet" in goal_lower:

            format_rules += """
- Output EXACTLY the requested number of numbered points
- Use ONLY this format:
  1.
  2.
  3.
- Never use "-" bullets
- Never use nested bullets
"""

        # =====================================
        # STEP 6: FINAL LLM EXECUTION
        # =====================================

        

        memory_text = ""

        if state.knowledge["memory"]:
        
            memory_text = (
                "\nKnown User Memory:\n"
                + "\n".join(
                    state.knowledge["memory"]
                )
                + "\n"
            )

        rag_text = ""

        if state.knowledge["rag"]:

            rag_text = "\nRetrieved Knowledge:\n\n"
        
            for chunk in state.knowledge["rag"]:
        
                rag_text += (
        
                    f"Document: {chunk['document']}\n"
        
                    f"Chunk: {chunk['chunk']}\n"
        
                    f"{chunk['text']}\n"
        
                    "----------------------------------------\n"

                )
        
        prompt = f"""
                {improvement_note}
                
                You are an execution agent.
                
                Use the retrieved knowledge ONLY when it is relevant
                to answering the user's request.
                
                {memory_text}
                
                {rag_text}
                
                User goal:
                {user_goal}
                
                Plan:
                {steps_text}
                
                Generate the FINAL ANSWER that EXACTLY matches
                the requested format.
                
                STRICT FORMAT RULES:
                
                {format_rules}
                """

        state.metrics["llm_calls"] += 1

        if state.knowledge["memory"]:

            state.add_trace(
                f"Memory Injected ({len(state.knowledge['memory'])})"
            )

        if state.knowledge["rag"]:

            state.add_trace(
        
                f"RAG Injected ({len(state.knowledge['rag'])})"
        
            )

        state.add_trace(
            "LLM Execution Started"
        )
        
        state.final_answer = (
            self.llm.generate(prompt).strip()
        )

        state.add_trace(
            "LLM Execution Completed"
        )

        state.add_trace(
            "Executor Completed"
        )