from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Note
from app.schemas import NoteCreate


def create_note(db: Session, note_data: NoteCreate, user_id: int) -> Note:
    note = Note(**note_data.model_dump(), user_id=user_id)

    db.add(note)
    db.commit()
    db.refresh(note)

    return note


def list_notes(
    db: Session,
    user_id: int,
    category_id: int | None = None,
    pattern: str | None = None,
) -> list[Note]:
    statement = select(Note).where(Note.user_id == user_id)

    if category_id is not None:
        statement = statement.where(Note.category_id == category_id)

    if pattern is not None:
        statement = statement.where(Note.pattern.ilike(f"%{pattern}%"))

    statement = statement.order_by(Note.id.desc())

    return list(db.scalars(statement).all())


def get_note_by_id(db: Session, note_id: int, user_id: int) -> Note | None:
    statement = select(Note).where(
        Note.id == note_id,
        Note.user_id == user_id,
    )

    return db.scalar(statement)


def get_note_by_question(db: Session, question: str, user_id: int) -> list[Note]:
    statement = select(Note).where(
        Note.user_id == user_id,
        Note.question.ilike(f"%{question}%"),
    )

    return list(db.scalars(statement).all())


def update_note(
    db: Session,
    note: Note,
    note_data: NoteCreate,
) -> Note:
    update_data = note_data.model_dump()

    for field, value in update_data.items():
        setattr(note, field, value)

    db.commit()
    db.refresh(note)

    return note


def delete_note(db: Session, note: Note) -> None:
    db.delete(note)
    db.commit()
