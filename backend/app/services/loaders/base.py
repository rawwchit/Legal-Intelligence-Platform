from abc import ABC, abstractmethod
from pathlib import Path

from langchain_core.documents import Document


class BaseLoader(ABC):
    @abstractmethod
    def load(self, file_path: Path) -> list[Document]:
        """Load a document and return LangChain Document objects."""
        raise NotImplementedError