from sentence_transformers import SentenceTransformer


class EmbeddingService:

    def __init__(self):
        self.model = SentenceTransformer(
            "BAAI/bge-small-en-v1.5"
        )
        self.normalize_embeddings = True

    def embed_documents(
        self,
        chunks: list[str]
    ) -> list[list[float]]:
        """
        Generate embeddings for a list of document chunks.
        """
        if not chunks:
            return []
        embeddings = self.model.encode(
            chunks,
            convert_to_numpy=True,
            normalize_embeddings=self.normalize_embeddings,
        )
        return embeddings.tolist()

    def embed_query(
        self,
        query: str
    ) -> list[float]:
        """
        Generate an embedding for a single query string.
        """
        if not query or not query.strip():
            raise ValueError("Query cannot be empty.")
        embedding = self.model.encode(
            query,
            convert_to_numpy=True,
            normalize_embeddings=self.normalize_embeddings,
        )
        return embedding.tolist()