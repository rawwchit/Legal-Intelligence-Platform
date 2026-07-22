from pathlib import Path

from bs4 import BeautifulSoup
from langchain_core.documents import Document
from markdown import markdown

from app.services.loaders.base import BaseLoader


class MarkdownLoader(BaseLoader):
    """Extract plain text from Markdown (.md) documents."""

    def load(self, file_path: Path) -> list[Document]:
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                md_content = file.read()

            html = markdown(md_content)
            text = BeautifulSoup(html, "html.parser").get_text(separator="\n")

            return [
                Document(
                    page_content=text.strip(),
                    metadata={
                        "source": str(file_path),
                        "file_type": "markdown",
                    },
                )
            ]

        except Exception as e:
            raise ValueError(
                f"Failed to load Markdown document: {file_path}"
            ) from e