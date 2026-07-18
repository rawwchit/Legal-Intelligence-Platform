from datetime import datetime
from pydantic import BaseModel, ConfigDict


class DocumentBase(BaseModel):
    title: str
    document_type: str
    court: str | None = None
    act_name: str | None = None
    year: int | None = None


class DocumentResponse(DocumentBase):
    id: int
    file_name: str
    file_path: str
    uploaded_by: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
    