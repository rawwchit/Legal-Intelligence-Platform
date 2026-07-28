from __future__ import annotations

from pathlib import Path

from app.services.parsing.base_parser import BaseParser
from app.services.parsing.constitution_parser import ConstitutionParser
from app.services.parsing.statute_parser import StatuteParser


class ParserFactory:
    """
    Returns the appropriate parser based on the legal document.
    """

    @staticmethod
    def get_parser(file_path: Path) -> BaseParser:
        filename = file_path.name.lower()

        if "constitution" in filename:
            return ConstitutionParser()

        return StatuteParser()