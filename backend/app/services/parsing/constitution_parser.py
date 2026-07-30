from __future__ import annotations

import re

from langchain_core.documents import Document
from app.services.parsing.parser_factory import ParserFactory
from app.services.parsing.base_parser import BaseParser
from app.services.parsing.models import (
    LegalDocumentNode,
    LegalDocumentType,
    LegalNodeType,
)

PART_PATTERN = re.compile(r"^PART\s+([IVXLCDM]+)", re.IGNORECASE)
CHAPTER_PATTERN = re.compile(r"^CHAPTER\s+([IVXLCDM]+)", re.IGNORECASE)
ARTICLE_PATTERN = re.compile(r"^Article\s+(\d+[A-Z]?)", re.IGNORECASE)


class ConstitutionParser(BaseParser):
    """Parser for the Constitution of India."""

    def parse(
        self,
        documents: list[Document],
    ) -> list[LegalDocumentNode]:
        nodes: list[LegalDocumentNode] = []

        current_part: str | None = None
        current_chapter: str | None = None

        for document in documents:
            for line in document.page_content.splitlines():
                line = line.strip()

                if not line:
                    continue

                if PART_PATTERN.match(line):
                    current_part = line
                    continue

                if CHAPTER_PATTERN.match(line):
                    current_chapter = line
                    continue

                article_match = ARTICLE_PATTERN.match(line)
                if not article_match:
                    continue

                article_number = article_match.group(1)

                nodes.append(
                    LegalDocumentNode(
                        id=f"constitution-article-{article_number}",
                        document_name="Constitution of India",
                        document_type=LegalDocumentType.CONSTITUTION,
                        node_type=LegalNodeType.ARTICLE,
                        number=article_number,
                        title=None,
                        content="",
                        metadata={
                            "part": current_part,
                            "chapter": current_chapter,
                            "source": document.metadata.get("source"),
                            "page": document.metadata.get("page"),
                        },
                    )
                )

        return nodes