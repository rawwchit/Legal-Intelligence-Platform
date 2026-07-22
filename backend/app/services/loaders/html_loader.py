from pathlib import Path

from bs4 import BeautifulSoup
from langchain_core.documents import Document

from app.services.loaders.base import BaseLoader


class HTMLLoader(BaseLoader):
    """Load HTML documents."""

    def load(self, file_path: Path) -> list[Document]:
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                html_content = file.read()

            soup = BeautifulSoup(html_content, "html.parser")
            text = soup.get_text(separator="\n").strip()

            return [
                Document(
                    page_content=text,
                    metadata={
                        "source": str(file_path),
                        "file_type": "html",
                    },
                )
            ]

        except Exception as e:
            raise ValueError(
                f"Failed to load HTML document: {file_path}"
            ) from e