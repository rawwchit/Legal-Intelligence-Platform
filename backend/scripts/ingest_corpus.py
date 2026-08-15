from pathlib import Path

from app.services.ingestion.ingestion_pipeline import IngestionPipeline
from app.services.embeddings.sentence_transformer_embedder import SentenceTransformerEmbedder
from app.services.vectorstores.qdrant_store import QdrantVectorStore
from app.core.config import settings


PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATASET_PATH = PROJECT_ROOT / "datasets" / "raw"
CHECKPOINT_PATH = (
    PROJECT_ROOT
    / "datasets"
    / "checkpoints"
    / "ingestion_checkpoint.json"
)


def main() -> None:
    print("=" * 60)
    print("Legal Intelligence Corpus Ingestion")
    print("=" * 60)

    pipeline = IngestionPipeline(
        dataset_path=DATASET_PATH,
        checkpoint_path=CHECKPOINT_PATH,
        embedder=SentenceTransformerEmbedder(),
        vector_store=QdrantVectorStore(
            url=settings.QDRANT_URL,
            collection_name=settings.QDRANT_COLLECTION_NAME,
        ),
    )

    pipeline.run()


if __name__ == "__main__":
    main()
