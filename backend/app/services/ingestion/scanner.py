from pathlib import Path
from typing import List

class DatasetScanner:
    """Recursively scans a datatset directory and return all supported files."""
    SUPPORTED_EXTENSIONS = {

        ".pdf",

        ".docx",

        ".txt",

        ".html",

        ".md",

        ".csv",

    }
    def __init__(self, dataset_path: str):
        self.dataset_path = Path(dataset_path)
    def scan(self) -> List[Path]:
        """
        Recursively scan for supported files.
        """
        if not self.dataset_path.exists():
            raise FileNotFoundError(
                f"Dataset directory not found: {self.dataset_path}"
            )
        files = []
        for file in self.dataset_path.rglob("*"):
            if (
                file.is_file()
                and file.suffix.lower() in self.SUPPORTED_EXTENSIONS
            ):
                files.append(file)
        return sorted(files)