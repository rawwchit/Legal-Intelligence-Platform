import csv
from pathlib import Path

from langchain_core.documents import Document

from app.services.loaders.base import BaseLoader


class CSVLoader(BaseLoader):
    """Extract plain text from CSV documents."""

    def load(self, file_path: Path) -> list[Document]:
        try:
            rows = []

            with open(file_path, "r", encoding="utf-8", newline="") as file:
                reader = csv.reader(file)

                for row in reader:
                    rows.append(" | ".join(cell.strip() for cell in row))

            return [
                Document(
                    page_content="\n".join(rows).strip(),
                    metadata={
                        "source": str(file_path),
                        "file_type": "csv",
                    },
                )
            ]

        except Exception as e:
            raise ValueError(
                f"Failed to load CSV document: {file_path}"
            ) from e