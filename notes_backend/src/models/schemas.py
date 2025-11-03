from datetime import datetime
from typing import List, Optional
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class NoteBase(BaseModel):
    """Shared fields for note models."""
    title: str = Field(..., min_length=1, max_length=256, description="Title of the note")
    content: str = Field("", description="Content of the note")
    tags: List[str] = Field(default_factory=list, description="List of tags")


class NoteCreate(NoteBase):
    """Payload for creating a note."""
    archived: bool = Field(default=False, description="Whether the note is archived")


class NoteUpdate(BaseModel):
    """Payload for updating a note (partial)."""
    title: Optional[str] = Field(default=None, min_length=1, max_length=256)
    content: Optional[str] = Field(default=None)
    tags: Optional[List[str]] = Field(default=None)
    archived: Optional[bool] = Field(default=None)


class NoteOut(NoteBase):
    """Representation of a note returned by the API."""
    id: UUID = Field(default_factory=uuid4, description="Unique identifier (UUID)")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Creation timestamp (UTC)")
    updated_at: datetime = Field(default_factory=datetime.utcnow, description="Last update timestamp (UTC)")
    archived: bool = Field(default=False, description="Whether the note is archived")

    class Config:
        from_attributes = True
