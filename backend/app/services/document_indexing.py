from __future__ import annotations

from collections.abc import Callable
from pathlib import Path
from typing import Any

from app.core.config import settings
from app.db.database import SessionLocal
from app.models.document import Document
from app.services.chunking.legal_chunker import LegalChunker
from app.services.embeddings.sentence_transformer_embedder import (
    SentenceTransformerEmbedder,
)
from app.services.loaders.loader_factory import LoaderFactory
from app.services.parsing.parser_factory import ParserFactory
from app.services.vectorstores.qdrant_store import QdrantVectorStore


class DocumentIndexingService:
    """Index an uploaded document independently of the request lifecycle."""

    def __init__(
        self,
        session_factory: Callable[[], Any] = SessionLocal,
        embedder: SentenceTransformerEmbedder | None = None,
        vector_store: QdrantVectorStore | None = None,
    ) -> None:
        self.session_factory = session_factory
        self.embedder = embedder
        self.vector_store = vector_store

    def index(self, document_id: int) -> None:
        db = self.session_factory()
        document = db.get(Document, document_id)
        if document is None:
            db.close()
            return

        document.indexing_status = "indexing"
        document.indexing_error = None
        db.commit()

        try:
            path = Path(document.file_path)
            documents = LoaderFactory.get_loader(path).load(path)
            nodes = ParserFactory.get_parser(path).parse(documents)
            chunks = LegalChunker().chunk(nodes)

            for chunk in chunks:
                chunk.id = f"document-{document.id}-{chunk.id}"
                chunk.metadata["document_id"] = document.id
                chunk.metadata["document_title"] = document.title

            if chunks:
                embedder = self.embedder or SentenceTransformerEmbedder()
                embeddings = embedder.embed([chunk.text for chunk in chunks])
                vector_store = self.vector_store or QdrantVectorStore(
                    url=settings.QDRANT_URL,
                    path=settings.QDRANT_PATH,
                    collection_name=settings.QDRANT_COLLECTION_NAME,
                    vector_size=len(embeddings[0]),
                )
                vector_store.upsert(chunks, embeddings)

            document.chunks_indexed = len(chunks)
            document.indexing_status = "indexed"
            db.commit()
        except Exception as error:
            db.rollback()
            document.indexing_status = "failed"
            document.indexing_error = str(error)[:1_000]
            db.commit()
        finally:
            db.close()
