from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app import models, schemas
from app.dependencies import get_db


router = APIRouter(
    prefix="/categories",
    tags=["Categories"],
)

DatabaseSession = Annotated[Session, Depends(get_db)]

# When a route asks for db: DatabaseSession

# FastAPI:
# calls get_db()
# receives the yielded session
# gives it to the route
# closes it afterward


@router.post(
    "/",
    response_model=schemas.CategoryRead,
    status_code=status.HTTP_201_CREATED,
)
def create_category(
    category_data: schemas.CategoryCreate,
    db: DatabaseSession,
):
    statement = select(models.Category).where(
        models.Category.name == category_data.name
    )

    existing_category = db.scalar(statement)

    if existing_category:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A category with this name already exists",
        )

    category = models.Category(
        name=category_data.name
    )

    db.add(category)
    db.commit()
    db.refresh(category)

    return category


@router.get(
    "/",
    response_model=list[schemas.CategoryRead],
    # This tells FastAPI:

    # what response structure is expected
    # which fields should be returned
    # how to validate and serialize the response

    # This is similar to serializing the result through a DRF serializer before returning it.
)
def list_categories(db: DatabaseSession):
    statement = select(models.Category).order_by(
        models.Category.name
    )

    categories = db.scalars(statement).all()

    return categories