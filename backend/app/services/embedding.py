from sentence_transformers import SentenceTransformer


class EmbeddingService:

    def __init__(self):
        self.model = SentenceTransformer(
            "BAAI/bge-small-en-v1.5"
        )

    def embed_documents(
        self,
        chunks: list[str]
    ) -> list[list[float]]:

        embeddings = self.model.encode(
            chunks,
            convert_to_numpy=True
        )

        return embeddings.tolist()

    def embed_query(
        self,
        query: str
    ) -> list[float]:

        embedding = self.model.encode(
            query,
            convert_to_numpy=True
        )

        return embedding.tolist()