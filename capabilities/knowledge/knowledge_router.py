class KnowledgeRouter:

    def route(
    self,
    query
  ):

        query = query.lower()
    
        memory_keywords = [
    
            "my ",
            "me ",
            "mine",
            "profession",
            "experience",
            "profile",
            "preference",
            "who am i"
    
        ]
    
        web_keywords = [
    
            "latest",
            "today",
            "current",
            "news",
            "announcement",
            "announcements",
            "recent",
            "live"
    
        ]
    
        # -------------------------
        # Memory query
        # -------------------------
    
        if any(k in query for k in memory_keywords):
    
            return ["memory"]
    
        # -------------------------
        # Latest information
        # -------------------------
    
        if any(k in query for k in web_keywords):
    
            return ["web"]
    
        # -------------------------
        # Everything else
        # -------------------------
    
        return ["rag", "web"]