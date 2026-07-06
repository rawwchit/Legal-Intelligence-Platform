from datetime import datetime
from app.db.database import Base
from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column
class User(Base):
    __tablename__ = "users"
    id:Mapped[int]=mapped_column(
        primary_key=True
        )
    username:Mapped[str] = mapped_column(
        unique=True
        )
    email:Mapped[str] = mapped_column(
        unique=True
    )
    hashed_password:Mapped[str] = mapped_column(
        
    )
    is_active:Mapped[bool] = mapped_column(
        default = True
    )
    created_at:Mapped[datetime] = mapped_column(
        server_default=func.now()
    )
    updated_at:Mapped[datetime] = mapped_column(
        server_default=func.now(),
        onupdate=func.now()
    )