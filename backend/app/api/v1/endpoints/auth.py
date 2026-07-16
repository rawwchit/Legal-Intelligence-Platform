from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.user import UserCreate, UserResponse, UserLogin
from app.core.security import hash_password, verify_password
from app.crud.user import (
    create_user,
    get_user_by_email,
    get_user_by_username,
)

router = APIRouter()


@router.post("/register", response_model=UserResponse)
def register(
    user: UserCreate,
    db: Session = Depends(get_db),
):
    existing_email = get_user_by_email(db, user.email)
    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered",
        )

    existing_username = get_user_by_username(db, user.username)
    if existing_username:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username already taken",
        )

    hashed_password = hash_password(user.password)

    db_user = create_user(
        db=db,
        username=user.username,
        email=user.email,
        hashed_password=hashed_password,
    )

    return db_user

@router.post("/login", response_model=UserResponse)

def login(
    user: UserLogin,
    db: Session = Depends(get_db),
):
    db_user = get_user_by_email(db, user.email)

    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    if not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    return db_user