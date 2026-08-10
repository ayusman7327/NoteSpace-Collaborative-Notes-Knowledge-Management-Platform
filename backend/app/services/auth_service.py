from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.core.security import (
    create_access_token,
    hash_password,
    verify_password,
)
from app.repositories.user_repository import (
    create_user,
    get_user_by_email,
)
from app.schemas.user import UserCreate, UserLogin


def register_user(
    db: Session,
    user_data: UserCreate
):
    email = user_data.email.lower().strip()

    existing_user = get_user_by_email(
        db=db,
        email=email,
    )

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="An account with this email already exists",
        )

    password_hash = hash_password(
        user_data.password
    )

    user = create_user(
        db=db,
        name=user_data.name.strip(),
        email=email,
        password_hash=password_hash,
    )

    return user


def login_user(
    db: Session,
    login_data: UserLogin
):
    email = login_data.email.lower().strip()

    user = get_user_by_email(
        db=db,
        email=email,
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    if not verify_password(
        login_data.password,
        user.password_hash,
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    access_token = create_access_token(
        user.id
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
    }