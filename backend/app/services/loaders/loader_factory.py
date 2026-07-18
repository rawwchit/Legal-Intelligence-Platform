from pathlib import Path

from app.services.loaders.docx_loader import DOCXLoader
from app.services.loaders.pdf_loader import PDFLoader
from app.services.loaders.txt_loader import TXTLoader
from app.services.loaders.markdown_loader import MarkdownLoader
from app.services.loaders.html_loader import HTMLLoader
from app.services.loaders.csv_loader import CSVLoader


class LoaderFactory:

    @staticmethod
    def get_loader(file_path: str):
        extension = Path(file_path).suffix.lower()

        loaders = {
            ".pdf": PDFLoader(),
            ".docx": DOCXLoader(),
            ".txt": TXTLoader(),
            ".md": MarkdownLoader(),
            ".html": HTMLLoader(),
            ".htm": HTMLLoader(),
            ".csv": CSVLoader(),
        }

        loader = loaders.get(extension)

        if loader is None:
            raise ValueError(f"Unsupported file type: {extension}")

        return loader