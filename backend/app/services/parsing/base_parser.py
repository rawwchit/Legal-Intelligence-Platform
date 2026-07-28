from __future__ import annotations

from abc import ABC, abstractmethod

from langchain_core.documents import Document

from app.services.parsing.models import LegalDocumentNode


class BaseParser(ABC):
    """
    Base class for every legal parser.
    """

    @abstractmethod
    def parse(
        self,
        documents: list[Document],
    ) -> list[LegalDocumentNode]:
        """
        Convert LangChain Documents into structured LegalDocumentNodes.
        """
        raise NotImplementedError