from fastapi import (
    APIRouter,
    BackgroundTasks,
    Depends,
    File,
    Form,
    HTTPException,
    UploadFile,
)
from sqlalchemy.orm import Session

from app.api.dependencies.roles import require_admin
from app.crud.document import create_document
from app.db.database import get_db
from app.models.user import User
from app.schemas.document import DocumentResponse
from app.services.storage import save_uploaded_file
from app.services.document_indexing import DocumentIndexingService
from app.crud.document import get_document

router = APIRouter()

@router.post(
    "/upload",
    response_model=DocumentResponse,
)
def upload_document(
    background_tasks: BackgroundTasks,
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

    background_tasks.add_task(DocumentIndexingService().index, document.id)

    return document


@router.get("/{document_id}/indexing-status", response_model=DocumentResponse)
def get_indexing_status(
    document_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    document = get_document(db, document_id)
    if document is None:
        raise HTTPException(status_code=404, detail="Document not found")
    return document
