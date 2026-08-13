from abc import ABC, abstractmethod


class BaseEmbedder(ABC):
    """Interface for legal text embedding implementations."""

    @abstractmethod
    def embed(self, texts: list[str]) -> list[list[float]]:
        """Convert text into embedding vectors."""
        raise NotImplementedError