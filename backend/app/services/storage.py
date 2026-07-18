import shutil
import uuid
from pathlib import Path

from fastapi import UploadFile

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)


def save_uploaded_file(file: UploadFile) -> tuple[str, str]:
    """
    Save an uploaded file to disk with a unique filename.

    Returns:
        tuple(file_name, file_path)
    """

    extension = Path(file.filename).suffix

    unique_name = f"{uuid.uuid4()}{extension}"

    file_path = UPLOAD_DIR / unique_name

    with file_path.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return unique_name, str(file_path)