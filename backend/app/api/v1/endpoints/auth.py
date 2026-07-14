from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.user import UserCreate, UserResponse

from app.core.security import hash_password
from app.crud.user import create_user

router = APIRouter()


@router.post("/register", response_model=UserResponse)
def register(
    user: UserCreate,
    db: Session = Depends(get_db),
):
    hashed_password = hash_password(user.password)
    db_user = create_user(
    db=db,
    username=user.username,
    email=user.email,
    hashed_password=hashed_password,
)
    return db_user