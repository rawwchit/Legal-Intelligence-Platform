

from __future__ import annotations

from typing import Any


class BatchIndexer:
    """Collect embeddings and upload them to the vector store in batches."""

    def __init__(self, vector_store: Any, batch_size: int = 500):
        self.vector_store = vector_store
        self.batch_size = batch_size

        self._embeddings: list[Any] = []
        self._chunks: list[str] = []
        self._metadata: list[dict] = []

    def add(self, embedding: Any, chunk: str, metadata: dict) -> None:
        self._embeddings.append(embedding)
        self._chunks.append(chunk)
        self._metadata.append(metadata)

        if len(self._embeddings) >= self.batch_size:
            self.flush()

    def flush(self) -> None:
        if not self._embeddings:
            return

        self.vector_store.upsert_embeddings(
            embeddings=self._embeddings,
            chunks=self._chunks,
            metadata=self._metadata,
        )

        self._embeddings.clear()
        self._chunks.clear()
        self._metadata.clear()

    def __len__(self) -> int:
        return len(self._embeddings)