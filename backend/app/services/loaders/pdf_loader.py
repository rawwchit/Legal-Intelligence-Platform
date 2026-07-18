import fitz

from app.services.loaders.base import BaseLoader


class PDFLoader(BaseLoader):
    """Extract text from PDF documents using PyMuPDF."""

    def extract_text(self, file_path: str) -> str:
        try:
            text = ""

            with fitz.open(file_path) as doc:
                for page in doc:
                    text += page.get_text()

            return text.strip()

        except Exception as e:
            raise ValueError(
                f"Failed to extract text from PDF: {file_path}"
            ) from e