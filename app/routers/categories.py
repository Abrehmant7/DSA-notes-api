from fastapi import APIRouter, status

from app.dependencies import CurrentUser, DatabaseSession
from app.schemas import CategoryCreate, CategoryRead
from app.services import category_service

router = APIRouter(
    prefix="/categories",
    tags=["Categories"],
)


@router.post(
    "/",
    response_model=CategoryRead,
    status_code=status.HTTP_201_CREATED,
)
def create_category(
    category_data: CategoryCreate,
    db: DatabaseSession,
    _current_user: CurrentUser,
):
    return category_service.create_category(db, category_data)


@router.get(
    "/",
    response_model=list[CategoryRead],
)
def list_categories(
    db: DatabaseSession,
    _current_user: CurrentUser,
):
    return category_service.list_categories(db)
