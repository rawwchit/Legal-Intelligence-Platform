

from __future__ import annotations

from pathlib import Path

from app.services.embedding import EmbeddingService
from app.services.indexing_service import IndexingService
from app.services.ingestion.batch_indexer import BatchIndexer
from app.services.ingestion.checkpoint_manager import CheckpointManager
from app.services.ingestion.metadata import MetadataExtractor
from app.services.ingestion.scanner import DatasetScanner


class IngestionPipeline:
    """Coordinates the end-to-end corpus ingestion workflow."""

    def __init__(
        self,
        dataset_path: str | Path,
        checkpoint_path: str | Path,
    ):
        self.dataset_path = Path(dataset_path)
        self.checkpoint_path = Path(checkpoint_path)

        self.scanner = DatasetScanner(self.dataset_path)
        self.metadata_extractor = MetadataExtractor(self.dataset_path)
        self.checkpoint_manager = CheckpointManager(self.checkpoint_path)

        self.indexing_service = IndexingService()
        self.embedding_service = EmbeddingService()
        self.batch_indexer = BatchIndexer(self.indexing_service.vector_store)

    def run(self) -> None:
        state = self.checkpoint_manager.load()
        files = self.scanner.scan()

        print(f"Found {len(files)} supported documents.")

        for file_path in files:
            metadata = self.metadata_extractor.extract(file_path)
            print(f"Queued: {metadata['relative_path']}")

            # TODO:
            # - Skip already indexed files using SHA256.
            # - Load document using LoaderFactory.
            # - Chunk document.
            # - Generate embeddings.
            # - Send batches to BatchIndexer.
            # - Persist checkpoint after each successful document.

        self.batch_indexer.flush()

        print("Corpus ingestion completed.")