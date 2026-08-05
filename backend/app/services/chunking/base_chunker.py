from __future__ import annotations

from abc import ABC, abstractmethod

from app.services.chunking.models import LegalChunk
from app.services.parsing.models import LegalDocumentNode


class BaseChunker(ABC):
    """
    Base interface for all legal chunkers.
    """

    @abstractmethod
    def chunk(
        self,
        nodes: list[LegalDocumentNode],
    ) -> list[LegalChunk]:
        """
        Convert LegalDocumentNodes into LegalChunks.
        """
        raise NotImplementedError