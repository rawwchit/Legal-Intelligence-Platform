from docx import Document

from app.services.loaders.base import BaseLoader


class DOCXLoader(BaseLoader):
    """Extract text from Microsoft Word (.docx) documents."""

    def extract_text(self, file_path: str) -> str:
        try:
            document = Document(file_path)

            paragraphs = [
                paragraph.text
                for paragraph in document.paragraphs
                if paragraph.text.strip()
            ]

            return "\n".join(paragraphs)

        except Exception as e:
            raise ValueError(
                f"Failed to extract text from DOCX: {file_path}"
            ) from e