from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app import models, schemas
from app.dependencies import get_db


router = APIRouter(
    prefix="/notes",
    tags=["Notes"],
)

DatabaseSession = Annotated[Session, Depends(get_db)]


@router.post(
    "/",
    response_model=schemas.NoteRead,
    status_code=status.HTTP_201_CREATED,
)
def create_note(
    note_data: schemas.NoteCreate,
    db: DatabaseSession,
):
    category = db.get(
        models.Category,
        note_data.category_id,
    )

    if category is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found",
        )

    note = models.Note(
        **note_data.model_dump()
    )

    db.add(note)
    db.commit()
    db.refresh(note)

    return note


@router.get(
    "/",
    response_model=list[schemas.NoteRead],
)
def list_notes(
    db: DatabaseSession,
    category_id: int | None = None,
    pattern: str | None = None,
):
    statement = select(models.Note)

    if category_id is not None:
        statement = statement.where(
            models.Note.category_id == category_id
        )

    if pattern is not None:
        statement = statement.where(
            models.Note.pattern.ilike(f"%{pattern}%")
        )

    statement = statement.order_by(
        models.Note.id.desc()
    )

    notes = db.scalars(statement).all()

    return notes


@router.get(
    "/{note_id}",
    response_model=schemas.NoteRead,
)
def retrieve_note(
    note_id: int,
    db: DatabaseSession,
):
    note = db.get(models.Note, note_id)

    if note is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Note not found",
        )

    return note


@router.put(
    "/{note_id}",
    response_model=schemas.NoteRead,
)
def update_note(
    note_id: int,
    note_data: schemas.NoteCreate,
    db: DatabaseSession,
):
    note = db.get(models.Note, note_id)

    if note is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Note not found",
        )

    category = db.get(
        models.Category,
        note_data.category_id,
    )

    if category is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found",
        )

    update_data = note_data.model_dump()

    for field, value in update_data.items():
        setattr(note, field, value)

    db.commit()
    db.refresh(note)

    return note


@router.delete(
    "/{note_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_note(
    note_id: int,
    db: DatabaseSession,
):
    note = db.get(models.Note, note_id)

    if note is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Note not found",
        )

    db.delete(note)
    db.commit()

    return None