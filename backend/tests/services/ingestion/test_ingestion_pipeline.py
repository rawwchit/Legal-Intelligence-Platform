from pathlib import Path

from app.services.ingestion.ingestion_pipeline import IngestionPipeline


def test_pipeline_returns_legal_chunks_without_indexing(tmp_path: Path) -> None:
    corpus = tmp_path / "corpus"
    corpus.mkdir()
    (corpus / "constitution_sample.txt").write_text(
        "Article 21. Protection of life\nNo person shall be deprived of life.",
        encoding="utf-8",
    )

    chunks = IngestionPipeline(
        dataset_path=corpus,
        checkpoint_path=tmp_path / "checkpoint.json",
    ).run()

    assert len(chunks) == 1
    assert chunks[0].metadata["article"] == "21"
    assert "No person shall be deprived of life." in chunks[0].text
