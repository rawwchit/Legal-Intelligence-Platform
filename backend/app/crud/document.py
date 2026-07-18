from sqlalchemy.orm import Session

from app.models.document import Document


def create_document(
    db: Session,
    title: str,
    file_name: str,
    file_path: str,
    document_type: str,
    uploaded_by: int,
    court: str | None = None,
    act_name: str | None = None,
    year: int | None = None,
):
    document = Document(
        title=title,
        file_name=file_name,
        file_path=file_path,
        document_type=document_type,
        court=court,
        act_name=act_name,
        year=year,
        uploaded_by=uploaded_by,
    )

    db.add(document)
    db.commit()
    db.refresh(document)

    return document