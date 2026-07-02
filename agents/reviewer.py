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
        # TOOL FAILURE DETECTION
        # =====================================

        if "Error:" in answer:

            if state:

                state.add_trace(
                    "Reviewer Rejected: Tool Failure"
                )

            return {
                "approved": False,
                "feedback": "Tool execution failed"
            }

        # =====================================
        # SENTENCE VALIDATION
        # =====================================

        if "sentence" in goal:

            if state:

                state.add_trace(
                    "Sentence Validation Started"
                )

            for line in answer.splitlines():

                stripped = line.strip()

                if re.match(r"^\d+\.", stripped):

                    if state:

                        state.add_trace(
                            "Sentence Validation Failed"
                        )

                    return {
                        "approved": False,
                        "feedback": "Sentences must not use numbering"
                    }

                if stripped.startswith("-"):

                    if state:

                        state.add_trace(
                            "Sentence Validation Failed"
                        )

                    return {
                        "approved": False,
                        "feedback": "Sentences must not use bullet points"
                    }

            match = re.search(
                r"(\d+)\s+sentence",
                goal
            )

            if match:

                expected = int(
                    match.group(1)
                )

                sentences = [
                    s.strip()
                    for s in re.split(
                        r"[.!?]+",
                        answer
                    )
                    if s.strip()
                ]

                if len(sentences) != expected:

                    if state:

                        state.add_trace(
                            f"Sentence Count Failed "
                            f"(expected={expected}, actual={len(sentences)})"
                        )

                    return {
                        "approved": False,
                        "feedback":
                        f"Expected exactly {expected} sentences"
                    }

            if state:

                state.add_trace(
                    "Sentence Validation Passed"
                )

        # =====================================
        # POINT VALIDATION
        # =====================================

        if "point" in goal or "bullet" in goal:

            if state:

                state.add_trace(
                    "Point Validation Started"
                )

            match = re.search(
                r"(\d+)",
                goal
            )

            if match:

                expected = int(
                    match.group(1)
                )

                actual = (
                    self._count_numbered_points(
                        answer
                    )
                )

                if actual != expected:

                    if state:

                        state.add_trace(
                            f"Point Count Failed "
                            f"(expected={expected}, actual={actual})"
                        )

                    return {
                        "approved": False,
                        "feedback":
                        f"Expected exactly {expected} numbered points"
                    }

            if state:

                state.add_trace(
                    "Point Validation Passed"
                )

        # =====================================
        # SEMANTIC VALIDATION
        # =====================================

        if state:

            state.add_trace(
                "Semantic Validation Started"
            )

        review_prompt = f"""
Evaluate whether this answer satisfies the user request.

User request:
{user_goal}

Answer:
{answer}

Return ONLY:
APPROVED
or
REJECTED
"""

        if state:

          state.metrics["llm_calls"] += 1

        response = (
                self.llm.generate(
                    review_prompt
                )
                .strip()
            )

        approved = (
            response.upper()
            .startswith("APPROVED")
        )

        # =====================================
        # FINAL DECISION
        # =====================================

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