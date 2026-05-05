from datetime import datetime as date
from pydantic import BaseModel as BM, Field

# Create a Note
class NoteCreate(BM):
    title: str | None = Field(None, max_length = 200, examples = ["Shopping List"])
    content: str = Field(..., min_length = 1, max_length = 10_000, examples = ["Buy milk, eggs, and bread"])

# Response when accessing a Note
class NoteResponse(BM):
    id: str
    title: str | None
    content: str
    created_at: date

    model_config = {"from_attributes": True}

# Error message for non-existant notes, etc.
class ErrorDetail(BM):
    detail: str