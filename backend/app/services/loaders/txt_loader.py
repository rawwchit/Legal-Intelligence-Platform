from app.services.loaders.base import BaseLoader


class TXTLoader(BaseLoader):

    def extract_text(self, file_path: str) -> str:
        """Extract text from plain text files."""
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                return file.read().strip()
        except Exception as e:
            raise ValueError(
                f"Failed to extract text from TXT: {file_path}"
            ) from e