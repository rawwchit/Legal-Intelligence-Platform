from app.services.embeddings.sentence_transformer_embedder import (
    SentenceTransformerEmbedder,
)


class EmbeddingService(SentenceTransformerEmbedder):
    """Backward-compatible embedding API using the shared retrieval model."""

    def embed_documents(
        self,
        chunks: list[str]
    ) -> list[list[float]]:
        """Generate embeddings for a list of legal text chunks."""
        return self.embed(chunks)
