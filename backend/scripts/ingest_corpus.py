from pathlib import Path

from app.services.ingestion.ingestion_pipeline import IngestionPipeline


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
    )

    pipeline.run()


if __name__ == "__main__":
    main()