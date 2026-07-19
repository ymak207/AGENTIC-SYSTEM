class IntentClassifier:

    def classify(
        self,
        query
    ):

        query = query.lower()

        knowledge_required = False

        compute_required = False

        # -------------------------
        # Compute
        # -------------------------

        math_tokens = [

            "+",
            "-",
            "*",
            "/",
            "%",
            "^"

        ]

        if any(token in query for token in math_tokens):

            compute_required = True

        # -------------------------
        # Knowledge
        # -------------------------

        knowledge_keywords = [

            "what",
            "who",
            "when",
            "where",
            "why",
            "how",
            "explain",
            "describe",
            "define",
            "tell",
            "show",
            "latest",
            "current",
            "today",
            "recent",
            "news",
            "announcement",
            "document",
            "pdf",
            "manual",
            "policy",
            "my ",
            "profession",
            "experience",
            "profile",
            "preference"

        ]

        if any(k in query for k in knowledge_keywords):

            knowledge_required = True

        return {

            "knowledge_required": knowledge_required,

            "compute_required": compute_required

        }