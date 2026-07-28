from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class LegalDocumentType(str, Enum):
    CONSTITUTION = "constitution"
    STATUTE = "statute"
    CASE_LAW = "case_law"
    REGULATION = "regulation"
    RULE = "rule"
    UNKNOWN = "unknown"


class LegalNodeType(str, Enum):
    DOCUMENT = "document"
    PART = "part"
    CHAPTER = "chapter"
    ARTICLE = "article"
    SECTION = "section"
    SUBSECTION = "subsection"
    CLAUSE = "clause"
    RULE = "rule"
    ORDER = "order"
    SCHEDULE = "schedule"
    EXPLANATION = "explanation"
    ILLUSTRATION = "illustration"
    PARAGRAPH = "paragraph"


@dataclass(slots=True)
class LegalDocumentNode:
    """
    Canonical representation of a legal document element.

    Every parser in the system must return LegalDocumentNode objects.
    """

    id: str

    document_name: str
    document_type: LegalDocumentType
    jurisdiction: str = "India"

    node_type: LegalNodeType = LegalNodeType.DOCUMENT

    number: str | None = None
    title: str | None = None

    content: str = ""

    parent: str | None = None
    children: list[str] = field(default_factory=list)

    metadata: dict[str, Any] = field(default_factory=dict)