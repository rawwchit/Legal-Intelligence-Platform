from langchain_text_splitters import RecursiveCharacterTextSplitter


class DocumentChunker:

    def __init__(
        self,
        chunk_size: int = 1000,
        chunk_overlap: int = 200,
    ):
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
        )

    def split_documents(self, documents):
        """Split LangChain Document objects while preserving metadata."""
        return self.splitter.split_documents(documents)

    def split_text(self, text: str) -> list[str]:
        """Split plain text into overlapping chunks."""
        if not text or not text.strip():
            return []

        return self.splitter.split_text(text)