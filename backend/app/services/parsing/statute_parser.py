from __future__ import annotations

import re

from langchain_core.documents import Document

from app.services.parsing.base_parser import BaseParser
from app.services.parsing.models import (
    LegalDocumentNode,
    LegalDocumentType,
    LegalNodeType,
)


SECTION_PATTERN = re.compile(r"^(?:Section\s+)?(\d+[A-Za-z]?)\s*[.\-:]\s*(.*)$", re.IGNORECASE)
SUBSECTION_PATTERN = re.compile(r"^\((\d+[A-Za-z]?)\)\s*(.*)$")
CLAUSE_PATTERN = re.compile(r"^\(([a-z]+)\)\s*(.*)$", re.IGNORECASE)


class StatuteParser(BaseParser):
    """Parse the numbered provisions of an Indian statute."""

    def parse(
        self,
        documents: list[Document],
    ) -> list[LegalDocumentNode]:
        nodes: list[LegalDocumentNode] = []
        document_name = self._document_name(documents)
        section: LegalDocumentNode | None = None
        subsection: LegalDocumentNode | None = None
        clause: LegalDocumentNode | None = None

        def append_text(node: LegalDocumentNode | None, line: str) -> None:
            if node is None:
                return
            node.content = f"{node.content}\n{line}".strip()

        for document in documents:
            source_metadata = {
                "source": document.metadata.get("source"),
                "source_page": document.metadata.get("page"),
            }
            for raw_line in document.page_content.splitlines():
                line = raw_line.strip()
                if not line:
                    continue

                section_match = SECTION_PATTERN.match(line)
                if section_match:
                    number, title = section_match.groups()
                    section = LegalDocumentNode(
                        id=f"statute-section-{number.lower()}",
                        document_name=document_name,
                        document_type=LegalDocumentType.STATUTE,
                        node_type=LegalNodeType.SECTION,
                        number=number,
                        title=title.strip() or None,
                        metadata={**source_metadata, "section": number},
                    )
                    nodes.append(section)
                    subsection = None
                    clause = None
                    continue

                subsection_match = SUBSECTION_PATTERN.match(line)
                if subsection_match and section is not None:
                    number, text = subsection_match.groups()
                    subsection = LegalDocumentNode(
                        id=f"{section.id}-subsection-{number.lower()}",
                        document_name=document_name,
                        document_type=LegalDocumentType.STATUTE,
                        node_type=LegalNodeType.SUBSECTION,
                        number=number,
                        content=text.strip(),
                        parent=section.id,
                        metadata={**source_metadata, "section": section.number, "subsection": number},
                    )
                    section.children.append(subsection.id)
                    nodes.append(subsection)
                    clause = None
                    continue

                clause_match = CLAUSE_PATTERN.match(line)
                if clause_match and subsection is not None:
                    number, text = clause_match.groups()
                    clause = LegalDocumentNode(
                        id=f"{subsection.id}-clause-{number.lower()}",
                        document_name=document_name,
                        document_type=LegalDocumentType.STATUTE,
                        node_type=LegalNodeType.CLAUSE,
                        number=number,
                        content=text.strip(),
                        parent=subsection.id,
                        metadata={
                            **source_metadata,
                            "section": section.number if section else None,
                            "subsection": subsection.number,
                            "clause": number,
                        },
                    )
                    subsection.children.append(clause.id)
                    nodes.append(clause)
                    continue

                append_text(clause or subsection or section, line)

        return nodes

    @staticmethod
    def _document_name(documents: list[Document]) -> str:
        if not documents:
            return "Unknown Statute"
        source = documents[0].metadata.get("source")
        if not source:
            return "Unknown Statute"
        return str(source).rsplit("/", maxsplit=1)[-1].rsplit(".", maxsplit=1)[0].replace("_", " ")
