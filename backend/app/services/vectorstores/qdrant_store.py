from __future__ import annotations

from app.services.vectorstores.base_vectorstore import BaseVectorStore


class QdrantVectorStore(BaseVectorStore):
    """
    Qdrant implementation of the vector store.
    """

    def __init__(self):
        pass

    def upsert(self, chunks, embeddings):
        raise NotImplementedError

    def search(self, embedding, limit=5):
        raise NotImplementedError