from fastapi import (
    APIRouter,
    Depends,
    File,
    Form,
    UploadFile,
)
from sqlalchemy.orm import Session

from app.api.dependencies.roles import require_admin
from app.crud.document import create_document
from app.db.database import get_db
from app.models.user import User
from app.schemas.document import DocumentResponse
from app.services.storage import save_uploaded_file
from app.services.indexing_service import IndexingService

router = APIRouter()

@router.post(
    "/upload",
    response_model=DocumentResponse,
)
def upload_document(
    title: str = Form(...),
    document_type: str = Form(...),
    court: str | None = Form(None),
    act_name: str | None = Form(None),
    year: int | None = Form(None),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    file_name, file_path = save_uploaded_file(file)

    document = create_document(
        db=db,
        title=title,
        file_name=file_name,
        file_path=file_path,
        document_type=document_type,
        court=court,
        act_name=act_name,
        year=year,
        uploaded_by=current_user.id,
    )

    indexing_service = IndexingService()

    chunk_count = indexing_service.index_document(
        file_path=file_path,
        document_id=document.id,
        filename=file_name,
    )

    print(f"Indexed {chunk_count} chunks for document {document.id}")

    return document