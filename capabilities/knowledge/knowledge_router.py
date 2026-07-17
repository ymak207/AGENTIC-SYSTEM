class KnowledgeRouter:

    def __init__(self):

        self.memory_keywords = [

            "my name",
            "my profession",
            "my job",
            "my role",
            "my profile",
            "my experience",
            "my skills",
            "my preference",
            "my preferences",
            "who am i",
            "about me"

        ]

        self.document_keywords = [

            "document",
            "documents",
            "pdf",
            "policy",
            "policies",
            "manual",
            "manuals",
            "uploaded",
            "upload",
            "knowledge base",
            "summarize",
            "summarise"

        ]

        self.latest_keywords = [

            "latest",
            "current",
            "today",
            "recent",
            "news",
            "announcement",
            "announcements",
            "live",
            "trending"

        ]

    def route(self, query):

        query = query.lower()

        # -------------------------
        # Personal
        # -------------------------

        if any(k in query for k in self.memory_keywords):

            sources = ["memory"]

            if any(k in query for k in self.latest_keywords):

                sources.append("web")

            return sources

        # -------------------------
        # Uploaded Documents
        # -------------------------

        if any(k in query for k in self.document_keywords):

            return ["rag"]

        # -------------------------
        # Latest Information
        # -------------------------

        if any(k in query for k in self.latest_keywords):

            return ["web"]

        # -------------------------
        # Default General Knowledge
        # -------------------------

        return ["rag", "web"]