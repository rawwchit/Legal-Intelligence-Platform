

import csv

from app.services.loaders.base import BaseLoader


class CSVLoader(BaseLoader):
    """Extract plain text from CSV documents."""

    def extract_text(self, file_path: str) -> str:
        try:
            rows = []

            with open(file_path, "r", encoding="utf-8", newline="") as file:
                reader = csv.reader(file)

                for row in reader:
                    rows.append(" | ".join(cell.strip() for cell in row))

            return "\n".join(rows).strip()

        except Exception as e:
            raise ValueError(
                f"Failed to extract text from CSV: {file_path}"
            ) from e