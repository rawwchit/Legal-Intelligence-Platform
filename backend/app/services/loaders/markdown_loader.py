
from markdown import markdown
from bs4 import BeautifulSoup

from app.services.loaders.base import BaseLoader


class MarkdownLoader(BaseLoader):
    """Extract plain text from Markdown (.md) documents."""

    def extract_text(self, file_path: str) -> str:
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                md_content = file.read()

            html = markdown(md_content)
            text = BeautifulSoup(html, "html.parser").get_text(separator="\n")

            return text.strip()

        except Exception as e:
            raise ValueError(
                f"Failed to extract text from Markdown: {file_path}"
            ) from e