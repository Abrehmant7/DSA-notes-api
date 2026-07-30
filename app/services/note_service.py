from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models import Note
from app.repositories import category_repository, note_repository
from app.schemas import NoteCreate


def create_note(db: Session, note_data: NoteCreate, user_id: int) -> Note:
    ensure_category_exists(db, note_data.category_id, user_id)

    return note_repository.create_note(db, note_data, user_id)


def list_notes(
    db: Session,
    user_id: int,
    category_id: int | None = None,
    pattern: str | None = None,
) -> list[Note]:
    return note_repository.list_notes(
        db=db,
        user_id=user_id,
        category_id=category_id,
        pattern=pattern,
    )


def retrieve_note(db: Session, note_id: int, user_id: int) -> Note:
    note = note_repository.get_note_by_id(db, note_id, user_id)

    if note is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Note not found",
        )

    return note

def search_notes(db: Session, question: str, user_id: int) -> list[Note]:
    notes = note_repository.get_note_by_question(db, question, user_id)

    if not notes:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Note not found",
        )

    return notes


def update_note(
    db: Session,
    note_id: int,
    note_data: NoteCreate,
    user_id: int
) -> Note:
    note = retrieve_note(db, note_id, user_id)
    ensure_category_exists(db, note_data.category_id, user_id)

    return note_repository.update_note(
        db=db,
        note=note,
        note_data=note_data,
    )


def delete_note(db: Session, note_id: int, user_id: int) -> None:
    note = retrieve_note(db, note_id, user_id)
    note_repository.delete_note(db, note)


def ensure_category_exists(db: Session, category_id: int, user_id: int) -> None:
    category = category_repository.get_category_by_id(db, category_id, user_id)

    if category is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found",
        )
