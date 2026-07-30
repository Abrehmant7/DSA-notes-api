from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.core import security
from app.models import User
from app.repositories import user_repository
from app.schemas import UserCreate


def register_user(db: Session, user_data: UserCreate) -> User:
    email = str(user_data.email).lower()
    existing_user = user_repository.get_user_by_email(db, email)

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A user with this email already exists",
        )

    hashed_password = security.hash_password(user_data.password)

    return user_repository.create_user(
        db=db,
        email=email,
        hashed_password=hashed_password,
    )


def authenticate_user(
    db: Session,
    email: str,
    password: str,
) -> User:
    user = user_repository.get_user_by_email(db, email.lower())

    if user is None or not security.verify_password(
        password,
        user.hashed_password,
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return user


def create_user_access_token(user: User) -> str:
    return security.create_access_token(subject=str(user.id))
