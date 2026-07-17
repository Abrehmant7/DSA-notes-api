from fastapi import APIRouter, status

from app.dependencies import CurrentUser, DatabaseSession
from app.schemas import NoteCreate, NoteRead
from app.services import note_service

router = APIRouter(
    prefix="/notes",
    tags=["Notes"],
)


@router.post(
    "/",
    response_model=NoteRead,
    status_code=status.HTTP_201_CREATED,
)
def create_note(
    note_data: NoteCreate,
    db: DatabaseSession,
    _current_user: CurrentUser,
):
    return note_service.create_note(db, note_data)


@router.get(
    "/",
    response_model=list[NoteRead],
)
def list_notes(
    db: DatabaseSession,
    _current_user: CurrentUser,
    category_id: int | None = None,
    pattern: str | None = None,
):
    return note_service.list_notes(
        db=db,
        category_id=category_id,
        pattern=pattern,
    )


@router.get(
    "/{note_id}",
    response_model=NoteRead,
)
def retrieve_note(
    note_id: int,
    db: DatabaseSession,
    _current_user: CurrentUser,
):
    return note_service.retrieve_note(db, note_id)


@router.put(
    "/{note_id}",
    response_model=NoteRead,
)
def update_note(
    note_id: int,
    note_data: NoteCreate,
    db: DatabaseSession,
    _current_user: CurrentUser,
):
    return note_service.update_note(
        db=db,
        note_id=note_id,
        note_data=note_data,
    )


@router.delete(
    "/{note_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_note(
    note_id: int,
    db: DatabaseSession,
    _current_user: CurrentUser,
):
    note_service.delete_note(db, note_id)

    return None
