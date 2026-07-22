from pathlib import Path
from app.services.loaders.base import BaseLoader

from app.services.loaders.docx_loader import DOCXLoader
from app.services.loaders.pdf_loader import PDFLoader
from app.services.loaders.txt_loader import TXTLoader
from app.services.loaders.markdown_loader import MarkdownLoader
from app.services.loaders.html_loader import HTMLLoader
from app.services.loaders.csv_loader import CSVLoader


class LoaderFactory:

    _LOADERS: dict[str, BaseLoader] = {
        ".pdf": PDFLoader(),
        ".docx": DOCXLoader(),
        ".txt": TXTLoader(),
        ".md": MarkdownLoader(),
        ".html": HTMLLoader(),
        ".htm": HTMLLoader(),
        ".csv": CSVLoader(),
    }

    @staticmethod
    def get_loader(file_path: Path) -> BaseLoader:
        extension = file_path.suffix.lower()

        loader = LoaderFactory._LOADERS.get(extension)

        if loader is None:
            raise ValueError(f"Unsupported file type: {extension}")

        return loader