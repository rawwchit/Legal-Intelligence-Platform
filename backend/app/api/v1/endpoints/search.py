from fastapi import APIRouter, HTTPException, Query

from app.core.config import settings
from app.services.embedding import EmbeddingService
from app.services.vectorstores.qdrant_store import QdrantVectorStore

router = APIRouter(tags=["Search"])


@router.get("/search")
def search_legal_corpus(
    query: str = Query(min_length=1, max_length=2_000),
    limit: int = Query(default=5, ge=1, le=50),
) -> list[dict]:
    """Return the most relevant indexed legal passages for a plain-text query."""
    try:
        embedding = EmbeddingService().embed_query(query)
        return QdrantVectorStore(
            url=settings.QDRANT_URL,
            path=settings.QDRANT_PATH,
            collection_name=settings.QDRANT_COLLECTION_NAME,
            vector_size=len(embedding),
        ).search(embedding, limit)
    except (ConnectionError, ValueError) as error:
        raise HTTPException(status_code=503, detail="Legal search is unavailable.") from error
