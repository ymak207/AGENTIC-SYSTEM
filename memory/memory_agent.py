import json
from pathlib import Path

from memory.embedding_model import (
    EmbeddingModel
)


class MemoryAgent:

    def __init__(self):

        self.memory_file = (
            Path(__file__).parent
            / "memory_store.json"
        )

        self.vector_file = (
            Path(__file__).parent
            / "vector_store.json"
        )

        self.embedding_model = (
            EmbeddingModel()
        )

        if not self.memory_file.exists():

            with open(
                self.memory_file,
                "w",
                encoding="utf-8"
            ) as file:

                json.dump(
                    {"facts": []},
                    file,
                    indent=4
                )

        if not self.vector_file.exists():

            with open(
                self.vector_file,
                "w",
                encoding="utf-8"
            ) as file:

                json.dump(
                    {"vectors": []},
                    file,
                    indent=4
                )

    def load_memory(self):

        with open(
            self.memory_file,
            "r",
            encoding="utf-8"
        ) as file:

            data = json.load(file)

        return data.get(
            "facts",
            []
        )

    def load_vectors(self):

        with open(
            self.vector_file,
            "r",
            encoding="utf-8"
        ) as file:

            data = json.load(file)

        return data.get(
            "vectors",
            []
        )
    
    def save_fact(
    self,
    fact: str
):

        memory = self.load_memory()
        vectors = self.load_vectors()
    
        fact_exists = fact in memory
    
        vector_exists = any(
            item["fact"] == fact
            for item in vectors
        )
    
        if not fact_exists:
    
            memory.append(fact)
    
            with open(
                self.memory_file,
                "w",
                encoding="utf-8"
            ) as file:
    
                json.dump(
                    {"facts": memory},
                    file,
                    indent=4
                )
    
        if not vector_exists:
    
            embedding = (
                self.embedding_model
                .embed(fact)
                .tolist()
            )
    
            vectors.append(
                {
                    "fact": fact,
                    "embedding": embedding
                }
            )
    
            with open(
                self.vector_file,
                "w",
                encoding="utf-8"
            ) as file:
    
                json.dump(
                    {"vectors": vectors},
                    file,
                    indent=4
            )
                
    def rebuild_vectors(self):

        memory = self.load_memory()
    
        vectors = []
    
        for fact in memory:
    
            embedding = (
                self.embedding_model
                .embed(fact)
                .tolist()
            )
    
            vectors.append(
                {
                    "fact": fact,
                    "embedding": embedding
                }
            )
    
        with open(
            self.vector_file,
            "w",
            encoding="utf-8"
        ) as file:
    
            json.dump(
                {"vectors": vectors},
                file,
                indent=4
            )
    
        print(
            f"Rebuilt {len(vectors)} vectors"
        )
        
    
    
    def get_relevant_memory(
    self,
    query: str,
    top_k: int = 3,
    threshold: float = 0.40
):

        query_embedding = (
            self.embedding_model
            .embed(query)
        )
    
        vectors = (
            self.load_vectors()
        )
    
        scored = []
    
        for item in vectors:
    
            score = (
                self.embedding_model
                .similarity(
                    query_embedding,
                    item["embedding"]
                )
            )
    
            scored.append(
                (
                    score,
                    item["fact"]
                )
            )
    
        scored.sort(
                reverse=True
            )

        filtered = []
        
        for score, fact in scored:
        
            if score >= threshold:
        
                filtered.append(
                    fact
                )
        
        return filtered[:top_k]