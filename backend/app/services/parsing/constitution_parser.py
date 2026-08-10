from __future__ import annotations

import re

from langchain_core.documents import Document

from app.services.parsing.base_parser import BaseParser
from app.services.parsing.models import (
    LegalDocumentNode,
    LegalDocumentType,
    LegalNodeType,
)

PART_PATTERN = re.compile(r"^PART\s+([IVXLCDM]+)\b", re.IGNORECASE)
CHAPTER_PATTERN = re.compile(r"^CHAPTER\s+([IVXLCDM]+)\b", re.IGNORECASE)
ARTICLE_PATTERN = re.compile(
    r"^(?:Article\s+)?(\d+[A-Z]?)\s*[.\-:]\s*(.*)$",
    re.IGNORECASE,
)


class ConstitutionParser(BaseParser):
    """Parser for the Constitution of India."""

    def parse(
        self,
        documents: list[Document],
    ) -> list[LegalDocumentNode]:
        nodes: list[LegalDocumentNode] = []

        current_part: str | None = None
        current_chapter: str | None = None
        article_number: str | None = None
        article_title: str | None = None
        article_body: list[str] = []
        article_metadata: dict[str, object] = {}

        def finish_article() -> None:
            if article_number is None:
                return

            content = "\n".join(article_body).strip()
            nodes.append(
                LegalDocumentNode(
                    id=f"constitution-article-{article_number.lower()}",
                    document_name="Constitution of India",
                    document_type=LegalDocumentType.CONSTITUTION,
                    node_type=LegalNodeType.ARTICLE,
                    number=article_number,
                    title=article_title,
                    content=content,
                    metadata=article_metadata.copy(),
                )
            )

        for document in documents:
            for line in document.page_content.splitlines():
                line = line.strip()

                if not line:
                    continue

                if PART_PATTERN.match(line):
                    finish_article()
                    article_number = None
                    article_title = None
                    article_body = []
                    current_part = line
                    continue

                if CHAPTER_PATTERN.match(line):
                    finish_article()
                    article_number = None
                    article_title = None
                    article_body = []
                    current_chapter = line
                    continue

                article_match = ARTICLE_PATTERN.match(line)
                if article_match:
                    finish_article()

                    article_number = article_match.group(1)
                    article_title = article_match.group(2).strip() or None
                    article_body = []
                    article_metadata = {
                        "part": current_part,
                        "chapter": current_chapter,
                        "source": document.metadata.get("source"),
                        "source_page": document.metadata.get("page"),
                    }
                    continue

                if article_number is not None:
                    article_body.append(line)

        finish_article()

        return nodes
