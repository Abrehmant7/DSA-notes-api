from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from app.dependencies import CurrentUser, DatabaseSession
from app.schemas import Token, UserCreate, UserRead
from app.services import auth_service

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.post(
    "/register",
    response_model=UserRead,
    status_code=201,
)
def register_user(
    user_data: UserCreate,
    db: DatabaseSession,
):
    return auth_service.register_user(db, user_data)


@router.post(
    "/login",
    response_model=Token,
)
def login_user(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: DatabaseSession,
):
    user = auth_service.authenticate_user(
        db=db,
        email=form_data.username,
        password=form_data.password,
    )
    access_token = auth_service.create_user_access_token(user)

    return {
        "access_token": access_token,
        "token_type": "bearer",
    }


@router.get(
    "/me",
    response_model=UserRead,
)
def read_current_user(current_user: CurrentUser):
    return current_user
