import json
from pathlib import Path

from memory.embedding_model import EmbeddingModel


class RAGVectorStore:

    def __init__(self):

        self.vector_file = (
            Path(__file__).parent
            / "rag_vectors.json"
        )

        self.embedding_model = (
            EmbeddingModel()
        )

        if not self.vector_file.exists():

            with open(
                self.vector_file,
                "w",
                encoding="utf-8"
            ) as file:

                json.dump(
                    {"chunks": []},
                    file,
                    indent=4
                )

    def load_vectors(self):

        with open(
            self.vector_file,
            "r",
            encoding="utf-8"
        ) as file:

            data = json.load(file)

        return data.get(
            "chunks",
            []
        )

    def save_vectors(
        self,
        vectors
    ):

        with open(
            self.vector_file,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                {
                    "chunks": vectors
                },
                file,
                indent=4
            )

    def build_index(
        self,
        chunks
    ):

        vectors = []

        for chunk in chunks:

            embedding = (
                self.embedding_model
                .embed(
                    chunk["text"]
                )
                .tolist()
            )

            vectors.append(
                {
                    "document": chunk["document"],
                    "chunk": chunk["chunk"],
                    "chunk_id": chunk["chunk_id"],
                    "word_count": chunk["word_count"],
                    "text": chunk["text"],
                    "embedding": embedding
                }
            )

        self.save_vectors(
            vectors
        )

        print()

        print(
            f"Indexed {len(vectors)} chunks."
        )

    def search(
        self,
        query,
        top_k=3,
        threshold=0.35
    ):

        query_embedding = (
            self.embedding_model
            .embed(query)
        )

        vectors = self.load_vectors()

        scored = []

        for item in vectors:

            score = (
                self.embedding_model
                .similarity(
                    query_embedding,
                    item["embedding"]
                )
            )

            if score >= threshold:

                scored.append(
                    (
                        score,
                        item
                    )
                )

        scored.sort(
            reverse=True,
            key=lambda x: x[0]
        )

        results = []

        for score, item in scored[:top_k]:
        
            result = item.copy()
        
            result["score"] = round(score, 4)
        
            results.append(result)
        
        return results
