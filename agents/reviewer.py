from llm.ollama_llm import OllamaLLM
import re


class ReviewerAgent:

    def __init__(self):

        self.llm = OllamaLLM()

    def _count_numbered_points(
        self,
        text: str
    ) -> int:
        """
        Count ONLY top-level numbered points.
        Example:

        1.
        2.
        3.
        """

        count = 0

        for line in text.splitlines():

            stripped = line.strip()

            if re.match(r"^\d+\.", stripped):

                count += 1

        return count

    def review(
    self,
    user_goal: str,
    answer: str,
    state=None
) -> dict:

        # =====================================
        # OBSERVABILITY
        # =====================================
    
        if state:
    
            state.add_trace(
                "Reviewer Started"
            )
    
        goal = user_goal.lower()
    
        # =====================================
        # TOOL FAILURE
        # =====================================
    
        if "error:" in answer.lower():
    
            if state:
    
                state.add_trace(
                    "Reviewer Rejected: Tool Failure"
                )
    
            return {
                "approved": False,
                "feedback": "Tool execution failed."
            }
    
        # =====================================
        # FORMAT VALIDATION
        # =====================================
    
        if "sentence" in goal:
    
            if state:
    
                state.add_trace(
                    "Sentence Validation Started"
                )
    
            for line in answer.splitlines():
    
                stripped = line.strip()
    
                if re.match(r"^\d+\.", stripped):
    
                    return {
                        "approved": False,
                        "feedback": "Do not use numbered sentences."
                    }
    
                if stripped.startswith("-"):
    
                    return {
                        "approved": False,
                        "feedback": "Do not use bullet points."
                    }
    
            match = re.search(
                r"(\d+)\s+sentence",
                goal
            )
    
            if match:
    
                expected = int(match.group(1))
    
                sentences = [
    
                    s.strip()
    
                    for s in re.split(
                        r"[.!?]+",
                        answer
                    )
    
                    if s.strip()
    
                ]
    
                if len(sentences) != expected:
    
                    return {
                        "approved": False,
                        "feedback":
                        f"Expected exactly {expected} sentences."
                    }
    
        elif "point" in goal or "bullet" in goal:
    
            if state:
    
                state.add_trace(
                    "Point Validation Started"
                )
    
            match = re.search(
                r"(\d+)",
                goal
            )
    
            if match:
    
                expected = int(match.group(1))
    
                actual = self._count_numbered_points(
                    answer
                )
    
                if actual != expected:
    
                    return {
                        "approved": False,
                        "feedback":
                        f"Expected exactly {expected} numbered points."
                    }
    
        # =====================================
        # LLM REVIEW
        # =====================================
    
        if state:
    
            state.add_trace(
                "Semantic Validation Started"
            )
    
            state.metrics["llm_calls"] += 1
    
        review_prompt = f"""
    You are a quality reviewer.
    
    Your job is NOT to fact-check.
    
    Assume any retrieved context and tool outputs are already correct.
    
    Only determine whether the answer satisfies the user's request.
    
    Approve if:
    - it answers the request
    - it follows the requested format
    - it is complete enough
    
    Reject only if:
    - it ignores part of the request
    - format is wrong
    - answer is incomplete
    - answer clearly contradicts itself
    
    User Request:
    {user_goal}
    
    Answer:
    {answer}
    
    Reply with ONLY one word.
    
    APPROVED
    
    or
    
    REJECTED
    """
    
        response = (
            self.llm.generate(
                review_prompt
            )
            .strip()
            .upper()
        )
    
        approved = response.startswith("APPROVED")
    
        if state:
    
            if approved:
    
                state.add_trace(
                    "Reviewer Approved"
                )
    
            else:
    
                state.add_trace(
                    "Reviewer Rejected"
                )
    
        return {
    
            "approved": approved,
    
            "feedback": response
    
        }