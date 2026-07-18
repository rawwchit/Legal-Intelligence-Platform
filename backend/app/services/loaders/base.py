from abc import ABC, abstractmethod


class BaseLoader(ABC):
    @abstractmethod
    def extract_text(self, file_path: str) -> str:
        """Extract plain text from a document."""
        pass