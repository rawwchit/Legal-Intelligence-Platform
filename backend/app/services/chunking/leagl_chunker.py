from __future__ import annotations

from app.services.chunking.base_chunker import BaseChunker
from app.services.chunking.models import ChunkType, LegalChunk
from app.services.parsing.models import LegalDocumentNode


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
            chunks.append(
                LegalChunk(
                    id=f"{node.id}-chunk-1",
                    node_id=node.id,
                    chunk_type=ChunkType(node.node_type.value),
                    text=node.content,
                    sequence=1,
                    metadata=node.metadata.copy(),
                )
            )

        return chunks