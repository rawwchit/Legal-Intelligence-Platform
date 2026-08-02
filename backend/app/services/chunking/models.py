from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class ChunkType(str, Enum):
    """Supported legal chunk types."""

    DOCUMENT = "document"
    ARTICLE = "article"
    SECTION = "section"
    SUBSECTION = "subsection"
    CLAUSE = "clause"
    RULE = "rule"
    PARAGRAPH = "paragraph"


@dataclass(slots=True)
class LegalChunk:
    """
    Canonical representation of a chunk that will be embedded
    and stored in the vector database.

    Every chunk originates from a LegalDocumentNode.
    """

    id: str

    node_id: str

    chunk_type: ChunkType

    text: str

    sequence: int = 0

    metadata: dict[str, Any] = field(default_factory=dict)