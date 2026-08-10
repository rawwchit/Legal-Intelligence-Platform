from app.services.chunking.legal_chunker import LegalChunker
from app.services.parsing.models import LegalDocumentNode, LegalDocumentType, LegalNodeType


def test_chunker_skips_structural_and_empty_nodes_and_preserves_context() -> None:
    nodes = [
        LegalDocumentNode(
            id="part-iii",
            document_name="Constitution of India",
            document_type=LegalDocumentType.CONSTITUTION,
            node_type=LegalNodeType.PART,
            content="PART III",
        ),
        LegalDocumentNode(
            id="article-21",
            document_name="Constitution of India",
            document_type=LegalDocumentType.CONSTITUTION,
            node_type=LegalNodeType.ARTICLE,
            number="21",
            title="Protection of life",
            content="No person shall be deprived of life.",
            metadata={"part": "PART III", "source_page": 42},
        ),
        LegalDocumentNode(
            id="empty-section",
            document_name="Sample Act",
            document_type=LegalDocumentType.STATUTE,
            node_type=LegalNodeType.SECTION,
        ),
    ]

    chunks = LegalChunker().chunk(nodes)

    assert len(chunks) == 1
    assert chunks[0].text.startswith("Article 21: Protection of life")
    assert chunks[0].metadata == {
        "document_name": "Constitution of India",
        "document_type": "constitution",
        "jurisdiction": "India",
        "part": "PART III",
        "source_page": 42,
        "article": "21",
        "title": "Protection of life",
    }
