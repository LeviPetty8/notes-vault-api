from datetime import datetime
from pydantic import BaseModel, Field

# Create a note
class NoteCreate(BaseModel):
    title: str | None = Field(None, max_length=200, examples=["Shopping list"])
    content: str = Field(..., min_length=1, max_length=10_000, examples=["Buy milk, eggs, bread"])

# Response when accessing a note
class NoteResponse(BaseModel):
    id: str
    title: str | None
    content: str
    created_at: datetime

    model_config = {"from_attributes": True}

# Error message when trying a forbidden method
class ErrorDetail(BaseModel):
    detail: str
