from sentence_transformers import SentenceTransformer

from app.services.embeddings.base_embedder import BaseEmbedder


class SentenceTransformerEmbedder(BaseEmbedder):
    """Generate embeddings using a Sentence Transformers model."""

    def __init__(
        self,
        model_name: str = "sentence-transformers/all-MiniLM-L6-v2",
    ) -> None:
        self.model = SentenceTransformer(model_name)

    def embed(self, texts: list[str]) -> list[list[float]]:
        """Generate embeddings for the supplied texts."""

        if not texts:
            return []

        embeddings = self.model.encode(
            texts,
            convert_to_numpy=True,
            show_progress_bar=False,
        )

        return embeddings.tolist()