from __future__ import annotations

from datetime import datetime
from typing import Dict, List, Optional
from uuid import UUID, uuid4

from ..models.schemas import NoteCreate, NoteOut, NoteUpdate


class InMemoryNotesRepository:
    """
    Simple in-memory repository for notes. This is intended for development
    and preview environments without persistence guarantees.
    """

    def __init__(self) -> None:
        # Use a dict for O(1) get/update/delete by id
        self._store: Dict[UUID, NoteOut] = {}

    # PUBLIC_INTERFACE
    def create(self, data: NoteCreate) -> NoteOut:
        """
        Create and store a new note.

        Args:
            data (NoteCreate): Data for the new note.

        Returns:
            NoteOut: The created note.
        """
        now = datetime.utcnow()
        note = NoteOut(
            id=uuid4(),
            title=data.title,
            content=data.content,
            tags=list(dict.fromkeys([t.strip() for t in data.tags if t.strip()])),
            created_at=now,
            updated_at=now,
            archived=bool(data.archived),
        )
        self._store[note.id] = note
        return note

    # PUBLIC_INTERFACE
    def get(self, note_id: UUID) -> Optional[NoteOut]:
        """
        Retrieve a note by id.

        Args:
            note_id (UUID): Note identifier.

        Returns:
            Optional[NoteOut]: The note if found, else None.
        """
        return self._store.get(note_id)

    # PUBLIC_INTERFACE
    def list(self, archived: Optional[bool] = None) -> List[NoteOut]:
        """
        List notes with optional archived filter.

        Args:
            archived (Optional[bool]): If provided, filter by archived status.

        Returns:
            List[NoteOut]: Notes list.
        """
        values = list(self._store.values())
        if archived is None:
            return sorted(values, key=lambda n: n.updated_at, reverse=True)
        return sorted([n for n in values if n.archived is archived], key=lambda n: n.updated_at, reverse=True)

    # PUBLIC_INTERFACE
    def update(self, note_id: UUID, patch: NoteUpdate) -> Optional[NoteOut]:
        """
        Update an existing note.

        Args:
            note_id (UUID): Note identifier.
            patch (NoteUpdate): Partial update payload.

        Returns:
            Optional[NoteOut]: Updated note or None if not found.
        """
        note = self._store.get(note_id)
        if not note:
            return None

        updated = note.model_copy(deep=True)
        if patch.title is not None:
            updated.title = patch.title
        if patch.content is not None:
            updated.content = patch.content
        if patch.tags is not None:
            updated.tags = list(dict.fromkeys([t.strip() for t in patch.tags if t.strip()]))
        if patch.archived is not None:
            updated.archived = bool(patch.archived)

        updated.updated_at = datetime.utcnow()
        self._store[note_id] = updated
        return updated

    # PUBLIC_INTERFACE
    def delete(self, note_id: UUID) -> bool:
        """
        Delete a note by id.

        Args:
            note_id (UUID): Note identifier.

        Returns:
            bool: True if deleted, False if not found.
        """
        return self._store.pop(note_id, None) is not None

    # PUBLIC_INTERFACE
    def set_archived(self, note_id: UUID, archived: bool) -> Optional[NoteOut]:
        """
        Set the archived status for a note.

        Args:
            note_id (UUID): Note identifier.
            archived (bool): Target archived status.

        Returns:
            Optional[NoteOut]: Updated note or None if not found.
        """
        note = self._store.get(note_id)
        if not note:
            return None
        patch = NoteUpdate(archived=archived)
        return self.update(note_id, patch)

    # PUBLIC_INTERFACE
    def search(self, q: Optional[str], tag: Optional[str], archived: Optional[bool]) -> List[NoteOut]:
        """
        Search notes by query across title and content, with optional tag and archived filters.

        Args:
            q (Optional[str]): Search text.
            tag (Optional[str]): Tag to filter on.
            archived (Optional[bool]): Archived filter.

        Returns:
            List[NoteOut]: Matching notes.
        """
        q_norm = (q or "").strip().lower()
        tag_norm = (tag or "").strip().lower() or None

        def match(note: NoteOut) -> bool:
            if archived is not None and note.archived is not archived:
                return False
            if tag_norm is not None and tag_norm not in [t.lower() for t in note.tags]:
                return False
            if q_norm:
                if q_norm in note.title.lower() or q_norm in note.content.lower():
                    return True
                return False
            return True

        results = [n for n in self._store.values() if match(n)]
        return sorted(results, key=lambda n: n.updated_at, reverse=True)
