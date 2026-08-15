from sentence_transformers import SentenceTransformer

from app.services.embeddings.base_embedder import BaseEmbedder

DEFAULT_EMBEDDING_MODEL = "BAAI/bge-small-en-v1.5"


class SentenceTransformerEmbedder(BaseEmbedder):
    """Generate embeddings using a Sentence Transformers model."""

    def __init__(
        self,
        model_name: str = DEFAULT_EMBEDDING_MODEL,
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
            normalize_embeddings=True,
        )

        return embeddings.tolist()

    def embed_query(self, query: str) -> list[float]:
        """Generate a normalized embedding for one legal search query."""
        if not query or not query.strip():
            raise ValueError("Query cannot be empty.")

        embedding = self.model.encode(
            query,
            convert_to_numpy=True,
            show_progress_bar=False,
            normalize_embeddings=True,
        )
        return embedding.tolist()
