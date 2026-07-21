

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


class CheckpointManager:
    """Persists ingestion progress so indexing jobs can resume safely."""

    def __init__(self, checkpoint_file: str | Path):
        self.checkpoint_file = Path(checkpoint_file)
        self.checkpoint_file.parent.mkdir(parents=True, exist_ok=True)

    def load(self) -> dict[str, Any]:
        if not self.checkpoint_file.exists():
            return {
                "last_processed_file": None,
                "documents_processed": 0,
                "chunks_indexed": 0,
            }

        with self.checkpoint_file.open("r", encoding="utf-8") as file:
            return json.load(file)

    def save(self, data: dict[str, Any]) -> None:
        with self.checkpoint_file.open("w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)

    def reset(self) -> None:
        if self.checkpoint_file.exists():
            self.checkpoint_file.unlink()