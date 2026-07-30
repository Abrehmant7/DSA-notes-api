from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Category


def get_category_by_name(db: Session, name: str, user_id: int) -> Category | None:
    statement = select(Category).where(
        Category.name == name,
        Category.user_id == user_id,
    )

    return db.scalar(statement)


def get_category_by_id(db: Session, category_id: int, user_id: int) -> Category | None:
    statement = select(Category).where(
        Category.id == category_id,
        Category.user_id == user_id,
    )

    return db.scalar(statement)


def list_categories(db: Session, user_id: int) -> list[Category]:
    statement = select(Category).where(Category.user_id == user_id).order_by(
        Category.name
    )

    return list(db.scalars(statement).all())


def create_category(db: Session, name: str, user_id: int) -> Category:
    category = Category(name=name, user_id=user_id)

    db.add(category)
    db.commit()
    db.refresh(category)

    return category
