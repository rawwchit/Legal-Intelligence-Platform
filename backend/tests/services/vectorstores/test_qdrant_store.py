from qdrant_client import QdrantClient

from app.services.chunking.models import ChunkType, LegalChunk
from app.services.vectorstores.qdrant_store import QdrantVectorStore


def test_upsert_and_search_chunks() -> None:
    store = QdrantVectorStore(
        collection_name="legal-test",
        vector_size=3,
        client=QdrantClient(":memory:"),
    )
    chunk = LegalChunk(
        id="article-21",
        node_id="article-21",
        chunk_type=ChunkType.ARTICLE,
        text="Article 21 protects life and liberty.",
        metadata={"article": "21"},
    )

    store.upsert([chunk], [[1.0, 0.0, 0.0]])

    results = store.search([1.0, 0.0, 0.0])

    assert results[0]["chunk_id"] == "article-21"
    assert results[0]["metadata"]["article"] == "21"


def test_upsert_rejects_mismatched_vectors() -> None:
    store = QdrantVectorStore(vector_size=3, client=QdrantClient(":memory:"))

    try:
        store.upsert([], [[1.0, 0.0, 0.0]])
    except ValueError as error:
        assert "exactly one embedding" in str(error)
    else:
        raise AssertionError("Expected a ValueError")


def test_uses_persistent_local_storage(tmp_path) -> None:
    store = QdrantVectorStore(
        collection_name="local-test",
        vector_size=3,
        path=str(tmp_path / "qdrant"),
    )

    assert store.client.collection_exists("local-test") is False
