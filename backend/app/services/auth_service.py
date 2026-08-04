from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.core.security import (
    create_access_token,
    hash_password,
    verify_password
)
from app.repositories.user_repository import (
    create_user,
    get_user_by_email
)
from app.schemas.auth import LoginRequest
from app.schemas.user import UserCreate


def register_user(db: Session, user_data: UserCreate):
    existing_user = get_user_by_email(db, user_data.email)

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="An account with this email already exists"
        )

    password_hash = hash_password(user_data.password)

    user = create_user(
        db=db,
        name=user_data.name.strip(),
        email=user_data.email.lower(),
        password_hash=password_hash
    )

    access_token = create_access_token(user.id)

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": user
    }


def login_user(db: Session, login_data: LoginRequest):
    user = get_user_by_email(
        db,
        login_data.email.lower()
    )

    if not user or not verify_password(
        login_data.password,
        user.password_hash
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    access_token = create_access_token(user.id)

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": user
    }