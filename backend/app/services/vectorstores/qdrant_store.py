
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, PointStruct, VectorParams

from app.core.config import settings


class QdrantVectorStore:
    """Wrapper around Qdrant for storing and searching embeddings."""

    def __init__(self):
        self.client = QdrantClient(path="storage/qdrant")
        self.collection_name = settings.QDRANT_COLLECTION_NAME

        collections = [c.name for c in self.client.get_collections().collections]
        if self.collection_name not in collections:
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(size=384, distance=Distance.COSINE),
            )

    def upsert_embeddings(self, embeddings, chunks, metadata):
        points = []

        for i, embedding in enumerate(embeddings):
            points.append(
                PointStruct(
                    id=metadata[i]["chunk_id"],
                    vector=embedding.tolist() if hasattr(embedding, "tolist") else embedding,
                    payload={
                        **metadata[i],
                        "text": chunks[i],
                    },
                )
            )

        if points:
            self.client.upsert(
                collection_name=self.collection_name,
                points=points,
            )

    def search(self, query_embedding, top_k: int = 5):
        vector = query_embedding.tolist() if hasattr(query_embedding, "tolist") else query_embedding

        return self.client.query_points(
            collection_name=self.collection_name,
            query=vector,
            limit=top_k,
            with_payload=True,
        )