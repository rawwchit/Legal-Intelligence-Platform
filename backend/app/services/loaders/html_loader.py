

from bs4 import BeautifulSoup

from app.services.loaders.base import BaseLoader


class HTMLLoader(BaseLoader):
    """Extract plain text from HTML documents."""

    def extract_text(self, file_path: str) -> str:
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                html_content = file.read()

            soup = BeautifulSoup(html_content, "html.parser")
            text = soup.get_text(separator="\n")

            return text.strip()

        except Exception as e:
            raise ValueError(
                f"Failed to extract text from HTML: {file_path}"
            ) from e