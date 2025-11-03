from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, HTTPException, Query, status
from pydantic import BaseModel, Field

from ...repository.notes_repository import InMemoryNotesRepository
from ...models.schemas import NoteCreate, NoteOut, NoteUpdate

# Single in-memory repository instance to persist state during app lifetime
repo = InMemoryNotesRepository()

router = APIRouter()


class SearchQuery(BaseModel):
    """Model to validate search query parameters internally."""
    q: Optional[str] = Field(default=None, description="Full text search in title and content")
    tag: Optional[str] = Field(default=None, description="Filter by a single tag")
    archived: Optional[bool] = Field(default=None, description="Filter by archived status")


@router.post(
    "",
    response_model=NoteOut,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new note",
    responses={
        201: {"description": "Note created successfully"},
        400: {"description": "Validation error"},
    },
)
# PUBLIC_INTERFACE
def create_note(payload: NoteCreate) -> NoteOut:
    """
    Create a new note.

    Args:
        payload (NoteCreate): The note data to create.

    Returns:
        NoteOut: The created note with generated id and timestamps.
    """
    note = repo.create(payload)
    return note


@router.get(
    "",
    response_model=List[NoteOut],
    summary="List notes",
    description="Retrieve all notes with optional filtering by archived status.",
)
# PUBLIC_INTERFACE
def list_notes(
    archived: Optional[bool] = Query(default=None, description="Filter by archived status"),
) -> List[NoteOut]:
    """
    List notes with optional archived filtering.

    Args:
        archived (Optional[bool]): If provided, filter by archived status.

    Returns:
        List[NoteOut]: List of notes.
    """
    return repo.list(archived=archived)


@router.get(
    "/{note_id}",
    response_model=NoteOut,
    summary="Get a note by id",
    responses={404: {"description": "Note not found"}},
)
# PUBLIC_INTERFACE
def get_note(note_id: UUID) -> NoteOut:
    """
    Retrieve a single note by its ID.

    Args:
        note_id (UUID): The note identifier.

    Returns:
        NoteOut: The requested note.
    """
    note = repo.get(note_id)
    if not note:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")
    return note


@router.put(
    "/{note_id}",
    response_model=NoteOut,
    summary="Update a note by id",
    responses={
        200: {"description": "Note updated successfully"},
        404: {"description": "Note not found"},
    },
)
# PUBLIC_INTERFACE
def update_note(note_id: UUID, payload: NoteUpdate) -> NoteOut:
    """
    Update a note.

    Args:
        note_id (UUID): The note identifier.
        payload (NoteUpdate): Fields to update.

    Returns:
        NoteOut: The updated note.
    """
    updated = repo.update(note_id, payload)
    if not updated:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")
    return updated


@router.delete(
    "/{note_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a note by id",
    responses={
        204: {"description": "Note deleted successfully"},
        404: {"description": "Note not found"},
    },
)
# PUBLIC_INTERFACE
def delete_note(note_id: UUID) -> None:
    """
    Delete a note.

    Args:
        note_id (UUID): The note identifier.

    Returns:
        None
    """
    ok = repo.delete(note_id)
    if not ok:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")


@router.patch(
    "/{note_id}/archive",
    response_model=NoteOut,
    summary="Archive or unarchive a note by id",
    description="Toggle a note's archived status. Provide archived=true to archive, false to unarchive.",
    responses={404: {"description": "Note not found"}},
)
# PUBLIC_INTERFACE
def archive_note(
    note_id: UUID,
    archived: bool = Query(..., description="Set to true to archive, false to unarchive"),
) -> NoteOut:
    """
    Archive or unarchive a note.

    Args:
        note_id (UUID): The note identifier.
        archived (bool): Target archived status.

    Returns:
        NoteOut: The updated note.
    """
    updated = repo.set_archived(note_id, archived)
    if not updated:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")
    return updated


@router.get(
    "/search",
    response_model=List[NoteOut],
    summary="Search notes",
    description="Search notes by text query across title and content, and optionally filter by tag and archived status.",
)
# PUBLIC_INTERFACE
def search_notes(
    q: Optional[str] = Query(default=None, description="Search string for title and content"),
    tag: Optional[str] = Query(default=None, description="Filter by one tag"),
    archived: Optional[bool] = Query(default=None, description="Filter by archived status"),
) -> List[NoteOut]:
    """
    Search notes by query, tag, and archived status.

    Args:
        q (Optional[str]): Text to search within title and content.
        tag (Optional[str]): Filter results that include this tag.
        archived (Optional[bool]): Filter by archived status.

    Returns:
        List[NoteOut]: Matching notes.
    """
    return repo.search(q=q, tag=tag, archived=archived)
