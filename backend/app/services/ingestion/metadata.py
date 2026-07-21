

from __future__ import annotations

from dataclasses import dataclass, asdict
from datetime import datetime
from hashlib import sha256
from pathlib import Path


@dataclass
class DocumentMetadata:
    filename: str
    extension: str
    relative_path: str
    file_size: int
    sha256: str
    created_at: str
    modified_at: str
    source: str = "corpus"


class MetadataExtractor:
    """Extract filesystem metadata used during ingestion."""

    def __init__(self, dataset_root: str | Path):
        self.dataset_root = Path(dataset_root).resolve()

    def extract(self, file_path: str | Path) -> dict:
        path = Path(file_path).resolve()
        stats = path.stat()

        metadata = DocumentMetadata(
            filename=path.name,
            extension=path.suffix.lower(),
            relative_path=str(path.relative_to(self.dataset_root)),
            file_size=stats.st_size,
            sha256=self._calculate_sha256(path),
            created_at=datetime.fromtimestamp(stats.st_ctime).isoformat(),
            modified_at=datetime.fromtimestamp(stats.st_mtime).isoformat(),
        )

        return asdict(metadata)

    @staticmethod
    def _calculate_sha256(path: Path) -> str:
        hasher = sha256()

        with path.open("rb") as file:
            for chunk in iter(lambda: file.read(1024 * 1024), b""):
                hasher.update(chunk)

        return hasher.hexdigest()