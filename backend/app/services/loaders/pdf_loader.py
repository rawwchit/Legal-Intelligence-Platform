from pathlib import Path

import fitz
from langchain_core.documents import Document

from app.services.loaders.base import BaseLoader


class PDFLoader(BaseLoader):
    """Extract text from PDF documents using PyMuPDF."""

    def load(self, file_path: Path) -> list[Document]:
        try:
            documents: list[Document] = []

            with fitz.open(file_path) as pdf:
                for page_number, page in enumerate(pdf, start=1):
                    text = page.get_text().strip()

                    if not text:
                        continue

                    documents.append(
                        Document(
                            page_content=text,
                            metadata={
                                "source": str(file_path),
                                "page": page_number,
                                "file_type": "pdf",
                            },
                        )
                    )

            return documents

        except Exception as e:
            raise ValueError(
                f"Failed to load PDF document: {file_path}"
            ) from e