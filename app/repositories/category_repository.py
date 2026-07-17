from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Category


def get_category_by_name(db: Session, name: str) -> Category | None:
    statement = select(Category).where(Category.name == name)

    return db.scalar(statement)


def get_category_by_id(db: Session, category_id: int) -> Category | None:
    return db.get(Category, category_id)


def list_categories(db: Session) -> list[Category]:
    statement = select(Category).order_by(Category.name)

    return list(db.scalars(statement).all())


def create_category(db: Session, name: str) -> Category:
    category = Category(name=name)

    db.add(category)
    db.commit()
    db.refresh(category)

    return category
