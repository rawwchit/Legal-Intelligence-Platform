from app.services.chunker import DocumentChunker
from app.services.embedding import EmbeddingService
from app.services.loaders.loader_factory import LoaderFactory
from app.services.vectorstores.qdrant_store import QdrantVectorStore


class IndexingService:
    """Coordinates the complete document indexing pipeline."""

    def __init__(self):
        self.chunker = DocumentChunker()
        self.embedding_service = EmbeddingService()
        self.vector_store = QdrantVectorStore()

    def index_document(
        self,
        file_path: str,
        document_id: int,
        filename: str,
    ) -> int:
        """Load, chunk, embed, and store a document in the vector database."""

        loader = LoaderFactory.get_loader(file_path)
        text = loader.extract_text(file_path)

        chunks = self.chunker.split_text(text)

        if not chunks:
            return 0

        embeddings = self.embedding_service.embed_documents(chunks)

        metadata = [
            {
                "chunk_id": f"doc-{document_id}-chunk-{i}",
                "document_id": document_id,
                "filename": filename,
                "chunk_index": i,
            }
            for i in range(len(chunks))
        ]

        self.vector_store.upsert_embeddings(
            embeddings=embeddings,
            chunks=chunks,
            metadata=metadata,
        )

        return len(chunks)