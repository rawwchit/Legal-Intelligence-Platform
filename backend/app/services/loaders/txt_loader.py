
from pathlib import Path

from langchain_core.documents import Document

from app.services.loaders.base import BaseLoader


class TXTLoader(BaseLoader):

    def load(self, file_path: Path) -> list[Document]:
        """Load a TXT file and return a list of LangChain Document objects."""
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                text = file.read().strip()

            return [
                Document(
                    page_content=text,
                    metadata={
                        "source": str(file_path),
                        "file_type": "txt",
                    },
                )
            ]
        except Exception as e:
            raise ValueError(
                f"Failed to load TXT document: {file_path}"
            ) from e