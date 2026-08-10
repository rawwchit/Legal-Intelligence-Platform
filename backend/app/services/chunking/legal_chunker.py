from __future__ import annotations

from app.services.chunking.base_chunker import BaseChunker
from app.services.chunking.models import ChunkType, LegalChunk
from app.services.parsing.models import LegalDocumentNode, LegalNodeType


STRUCTURAL_NODE_TYPES = {LegalNodeType.PART, LegalNodeType.CHAPTER}


class LegalChunker(BaseChunker):
    """
    Default legal chunker.

    Currently creates one chunk per LegalDocumentNode.
    """

    def chunk(
        self,
        nodes: list[LegalDocumentNode],
    ) -> list[LegalChunk]:

        chunks: list[LegalChunk] = []

        for node in nodes:
            if node.node_type in STRUCTURAL_NODE_TYPES:
                continue

            text = self._chunk_text(node)
            if not text:
                continue

            try:
                chunk_type = ChunkType(node.node_type.value)
            except ValueError:
                # Nodes such as schedules and illustrations need dedicated
                # chunking rules before they become searchable content.
                continue

            metadata = {
                "document_name": node.document_name,
                "document_type": node.document_type.value,
                "jurisdiction": node.jurisdiction,
                **node.metadata,
            }
            if node.number:
                metadata.setdefault(node.node_type.value, node.number)
            if node.title:
                metadata.setdefault("title", node.title)

            chunks.append(
                LegalChunk(
                    id=f"{node.id}-chunk-1",
                    node_id=node.id,
                    chunk_type=chunk_type,
                    text=text,
                    sequence=1,
                    metadata=metadata,
                )
            )

        return chunks

    @staticmethod
    def _chunk_text(node: LegalDocumentNode) -> str:
        """Build standalone retrieval text without producing empty chunks."""
        heading = " ".join(part for part in (node.node_type.value.title(), node.number or "") if part)
        if node.title:
            heading = f"{heading}: {node.title}" if heading else node.title
        body = node.content.strip()
        if not body:
            return ""
        return f"{heading}\n\n{body}" if heading else body
