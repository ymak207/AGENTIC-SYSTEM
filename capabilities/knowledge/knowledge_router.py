import re

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

    def requires_knowledge(self, query):
    
        query = query.lower()
    
        if any(k in query for k in self.memory_keywords):
            return True
    
        if any(k in query for k in self.document_keywords):
            return True
    
        if any(k in query for k in self.latest_keywords):
            return True
    
        # Pure math expression only
        if re.fullmatch(r"[\d\s\+\-\*/().]+", query.strip()):
            return False
    
        # Everything else is treated as knowledge
        return True