from __future__ import annotations

from uuid import NAMESPACE_URL, uuid5

from qdrant_client import QdrantClient, models

from app.services.chunking.models import LegalChunk
from app.services.vectorstores.base_vectors import BaseVectorStore


class QdrantVectorStore(BaseVectorStore):
    """
    Qdrant implementation of the vector store.
    """

    def __init__(
        self,
        url: str | None = None,
        collection_name: str = "legal-intelligence",
        vector_size: int = 384,
        client: QdrantClient | None = None,
    ) -> None:
        self.collection_name = collection_name
        self.vector_size = vector_size
        self.client = client or QdrantClient(url=url or "http://localhost:6333")

    def _ensure_collection(self) -> None:
        if not self.client.collection_exists(self.collection_name):
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=models.VectorParams(
                    size=self.vector_size,
                    distance=models.Distance.COSINE,
                ),
            )

    def upsert(
        self,
        chunks: list[LegalChunk],
        embeddings: list[list[float]],
    ) -> None:
        if len(chunks) != len(embeddings):
            raise ValueError("Each chunk must have exactly one embedding.")
        if not chunks:
            return
        if any(len(vector) != self.vector_size for vector in embeddings):
            raise ValueError(f"Embeddings must contain {self.vector_size} dimensions.")

        self._ensure_collection()
        points = [
            models.PointStruct(
                id=str(uuid5(NAMESPACE_URL, chunk.id)),
                vector=embedding,
                payload={
                    "chunk_id": chunk.id,
                    "node_id": chunk.node_id,
                    "chunk_type": chunk.chunk_type.value,
                    "text": chunk.text,
                    "sequence": chunk.sequence,
                    "metadata": chunk.metadata,
                },
            )
            for chunk, embedding in zip(chunks, embeddings, strict=True)
        ]
        self.client.upsert(collection_name=self.collection_name, points=points, wait=True)

    def search(self, embedding: list[float], limit: int = 5) -> list[dict]:
        if not embedding:
            return []
        if len(embedding) != self.vector_size:
            raise ValueError(f"Query embedding must contain {self.vector_size} dimensions.")
        if limit < 1:
            raise ValueError("Search limit must be at least 1.")
        if not self.client.collection_exists(self.collection_name):
            return []

        response = self.client.query_points(
            collection_name=self.collection_name,
            query=embedding,
            limit=limit,
            with_payload=True,
        )
        return [
            {"score": point.score, **(point.payload or {})}
            for point in response.points
        ]
