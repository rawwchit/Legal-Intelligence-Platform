from __future__ import annotations

from abc import ABC, abstractmethod

from app.services.chunking.models import LegalChunk


class BaseVectorStore(ABC):
    """
    Abstract interface for vector database implementations.
    """

    @abstractmethod
    def upsert(
        self,
        chunks: list[LegalChunk],
        embeddings: list[list[float]],
    ) -> None:
        """
        Store chunks and their embeddings.
        """
        raise NotImplementedError

    @abstractmethod
    def search(
        self,
        embedding: list[float],
        limit: int = 5,
    ):
        """
        Search for similar vectors.
        """
        raise NotImplementedError