from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models import Category
from app.repositories import category_repository
from app.schemas import CategoryCreate


def create_category(
    db: Session,
    category_data: CategoryCreate,
) -> Category:
    existing_category = category_repository.get_category_by_name(
        db,
        category_data.name,
    )

    if existing_category:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A category with this name already exists",
        )

    return category_repository.create_category(
        db,
        category_data.name,
    )


def list_categories(db: Session) -> list[Category]:
    return category_repository.list_categories(db)
