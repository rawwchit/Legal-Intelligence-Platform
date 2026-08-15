from types import SimpleNamespace
from unittest.mock import Mock, patch

from app.services.chunking.models import ChunkType, LegalChunk
from app.services.document_indexing import DocumentIndexingService


def test_indexes_uploaded_document_and_records_status() -> None:
    document = SimpleNamespace(
        id=7,
        title="Test Act",
        file_path="test.txt",
        indexing_status="pending",
        indexing_error=None,
        chunks_indexed=0,
    )
    db = Mock()
    db.get.return_value = document
    chunk = LegalChunk(
        id="section-1",
        node_id="section-1",
        chunk_type=ChunkType.SECTION,
        text="Section 1. Test provision.",
    )
    loader = Mock()
    loader.load.return_value = [Mock()]
    parser = Mock()
    parser.parse.return_value = [Mock()]
    chunker = Mock()
    chunker.chunk.return_value = [chunk]
    embedder = Mock()
    embedder.embed.return_value = [[0.1, 0.2, 0.3]]
    vector_store = Mock()

    with (
        patch("app.services.document_indexing.LoaderFactory.get_loader", return_value=loader),
        patch("app.services.document_indexing.ParserFactory.get_parser", return_value=parser),
        patch("app.services.document_indexing.LegalChunker", return_value=chunker),
    ):
        DocumentIndexingService(
            session_factory=Mock(return_value=db),
            embedder=embedder,
            vector_store=vector_store,
        ).index(document.id)

    assert document.indexing_status == "indexed"
    assert document.chunks_indexed == 1
    assert chunk.id == "document-7-section-1"
    assert chunk.metadata["document_id"] == 7
    vector_store.upsert.assert_called_once_with([chunk], [[0.1, 0.2, 0.3]])
    db.close.assert_called_once()
