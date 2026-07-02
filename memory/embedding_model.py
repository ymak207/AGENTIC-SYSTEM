from sentence_transformers import (
    SentenceTransformer
)
from numpy import dot
from numpy.linalg import norm


class EmbeddingModel:

    def __init__(self):

        self.model = SentenceTransformer(
            "all-MiniLM-L6-v2"
        )

    def embed(
        self,
        text: str
    ):

        return self.model.encode(
            text
        )

    def similarity(
        self,
        emb1,
        emb2
    ):

        return float(
            dot(emb1, emb2)
            /
            (
                norm(emb1)
                *
                norm(emb2)
            )
        )