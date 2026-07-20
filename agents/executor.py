from llm.ollama_llm import OllamaLLM

from capabilities.knowledge.knowledge_executor import KnowledgeExecutor
from capabilities.compute.compute_executor import ComputeExecutor


class ExecutorAgent:

    def __init__(self):

        self.llm = OllamaLLM()
    
        self.executors = {
    
            "knowledge": KnowledgeExecutor(),
    
            "compute": ComputeExecutor()
    
        }
    
        self.knowledge_executor = self.executors["knowledge"]

    def execute(self, plan: dict, state, user_goal: str):

        # =====================================
        # OBSERVABILITY
        # =====================================

        state.add_trace(
                "Executor Started"
        )

        for step in plan["steps"]:

            capability = step["capability"]
        
            state.add_trace(
                f"Executing capability: {capability}"
            )
        
            executor = self.executors.get(
                capability
            )
        
            if executor is None:
        
                raise Exception(
                    f"Unknown capability {capability}"
                )
        
            executor.execute(
        
                step=step,
        
                state=state,
        
                user_goal=user_goal
        
            )
        
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

        web_text = ""
        
        compute_text = ""

        if hasattr(state, "compute_results"):
        
            if state.compute_results:
        
                compute_text = "\nComputed Results:\n"
        
                for item in state.compute_results:
        
                    compute_text += (
        
                        f"{item['expression']} = {item['result']}\n"
        
                    )
        
                compute_text += "\n"

        if state.knowledge["rag"]:

            rag_text = "\nRetrieved Knowledge:\n\n"
        
            for chunk in state.knowledge["rag"]:
        
                rag_text += (
        
                    f"Document: {chunk['document']}\n"
        
                    f"Chunk: {chunk['chunk']}\n"
        
                    f"{chunk['text']}\n"
        
                    "----------------------------------------\n"

                )
        
        if state.knowledge["web"]:

            web_text = "\nRetrieved Web Results:\n\n"
        
            for item in state.knowledge["web"]:
        
                web_text += (
        
                    f"Title: {item['title']}\n"
        
                    f"{item['content']}\n"
        
                    "----------------------------------------\n"
        
                )
        
        
        prompt = f"""
                {improvement_note}
                
                You are an execution agent.
                
                Use the available information when appropriate.

                Priority order:
                
                1. User Memory
                2. Retrieved RAG Knowledge
                3. Retrieved Web Results
                4. Computed Results
                
                If multiple sources contain the answer,
                prefer the higher priority source.
                
                Never invent facts.
                
                If Computed Results are present,
                use those values exactly.
                
                Do NOT recompute mathematical expressions yourself.
                
                {memory_text}

                {rag_text}
                
                {web_text}
                
                {compute_text}
                
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

        if state.knowledge["web"]:

            state.add_trace(
        
                f"Web Injected ({len(state.knowledge['web'])})"
        
            )

        if hasattr(state, "compute_results"):

            if state.compute_results:
        
                state.add_trace(
        
                    f"Compute Injected ({len(state.compute_results)})"
        
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