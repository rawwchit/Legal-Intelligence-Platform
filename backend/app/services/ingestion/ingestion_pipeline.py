from __future__ import annotations

from pathlib import Path

from app.services.chunking.legal_chunker import LegalChunker
from app.services.ingestion.checkpoint_manager import CheckpointManager
from app.services.ingestion.metadata import MetadataExtractor
from app.services.ingestion.scanner import DatasetScanner
from app.services.loaders.loader_factory import LoaderFactory
from app.services.parsing.parser_factory import ParserFactory


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

        self.chunker = LegalChunker()

    def run(self) -> list:
        """Load, parse, and chunk corpus files; indexing is intentionally disabled."""
        self.checkpoint_manager.load()
        files = self.scanner.scan()

        print(f"Found {len(files)} supported documents.")

        loaded_files = 0
        loaded_documents = 0
        chunks = []

        for file in files:
            loader = LoaderFactory.get_loader(file)
            documents = loader.load(file)

            loaded_files += 1
            loaded_documents += len(documents)

            parser = ParserFactory.get_parser(file)
            nodes = parser.parse(documents)
            file_chunks = self.chunker.chunk(nodes)
            chunks.extend(file_chunks)

            print(
                f"Loaded: {file.name} -> {len(documents)} document(s), "
                f"{len(nodes)} legal node(s), {len(file_chunks)} chunk(s)"
            )

        print("\nIngestion Summary")
        print("-" * 40)
        print(f"Files scanned     : {len(files)}")
        print(f"Files loaded      : {loaded_files}")
        print(f"Documents created : {loaded_documents}")
        print(f"Legal chunks      : {len(chunks)}")
        print("-" * 40)
        print("Corpus parsing and chunking completed; indexing is disabled.")
        return chunks
