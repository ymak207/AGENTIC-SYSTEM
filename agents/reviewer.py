from llm.ollama_llm import OllamaLLM
import re


class ReviewerAgent:
    def __init__(self):
        self.llm = OllamaLLM()

    def _count_numbered_points(self, text: str) -> int:
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

    def review(self, user_goal: str, answer: str) -> dict:

        goal = user_goal.lower()

        if "Error:" in answer:
            return {
                "approved": False,
                "feedback": "Tool execution failed"
            }

        # =========================
        # SENTENCE VALIDATION
        # =========================

        if "sentence" in goal:

            # reject numbering/bullets
            for line in answer.splitlines():

                stripped = line.strip()

                if re.match(r"^\d+\.", stripped):
                    return {
                        "approved": False,
                        "feedback": "Sentences must not use numbering"
                    }

                if stripped.startswith("-"):
                    return {
                        "approved": False,
                        "feedback": "Sentences must not use bullet points"
                    }

            match = re.search(r"(\d+)\s+sentence", goal)

            if match:

                expected = int(match.group(1))

                sentences = [
                    s.strip()
                    for s in re.split(r"[.!?]+", answer)
                    if s.strip()
                ]

                if len(sentences) != expected:
                    return {
                        "approved": False,
                        "feedback": f"Expected exactly {expected} sentences"
                    }

        # =========================
        # POINT VALIDATION
        # =========================

        if "point" in goal or "bullet" in goal:

            match = re.search(r"(\d+)", goal)

            if match:

                expected = int(match.group(1))

                actual = self._count_numbered_points(answer)

                if actual != expected:
                    return {
                        "approved": False,
                        "feedback": f"Expected exactly {expected} numbered points"
                    }

        # =========================
        # SEMANTIC VALIDATION
        # =========================

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

        response = self.llm.generate(review_prompt).strip()

        approved = response.upper().startswith("APPROVED")

        return {
            "approved": approved,
            "feedback": response
        }