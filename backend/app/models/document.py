from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.db.database import Base


class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)

    title = Column(String, nullable=False)

    file_name = Column(String, nullable=False)

    file_path = Column(String, nullable=False)

    document_type = Column(String, nullable=False)

    court = Column(String, nullable=True)

    act_name = Column(String, nullable=True)

    year = Column(Integer, nullable=True)

    uploaded_by = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    indexing_status = Column(String, nullable=False, server_default="pending")

    chunks_indexed = Column(Integer, nullable=False, server_default="0")

    indexing_error = Column(String, nullable=True)

    uploader = relationship("User")
