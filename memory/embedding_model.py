from sentence_transformers import SentenceTransformer
from numpy import dot
from numpy.linalg import norm


class EmbeddingModel:
    """
    Singleton wrapper around SentenceTransformer.

    The embedding model is loaded only once
    and reused across the entire application.
    """

    _model = None

    def __init__(self):

        if EmbeddingModel._model is None:

            print(
                "\nLoading embedding model (one time)...\n"
            )

            EmbeddingModel._model = SentenceTransformer(
                "all-MiniLM-L6-v2"
            )

        self.model = EmbeddingModel._model

    def embed(
        self,
        text: str
    ):

        return self.model.encode(text)

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