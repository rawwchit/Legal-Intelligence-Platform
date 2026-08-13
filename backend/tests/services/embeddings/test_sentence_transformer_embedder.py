from app.services.embeddings.sentence_transformer_embedder import (
    SentenceTransformerEmbedder,
)


def test_empty_text_returns_empty_embeddings():
    embedder = SentenceTransformerEmbedder()

    assert embedder.embed([]) == []


def test_embed_returns_vectors():
    embedder = SentenceTransformerEmbedder()

    embeddings = embedder.embed(
        ["Article 21 protects life and personal liberty."]
    )

    assert len(embeddings) == 1
    assert len(embeddings[0]) > 0