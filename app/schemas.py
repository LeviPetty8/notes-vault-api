from datetime import datetime as date
from pydantic import BaseModel as BM, Field

class NoteCreate(BM):
    title: str | None = Field(None, max_length = 200, examples = ["Shopping List"])
    content: str = Field(..., min_length = 1, max_length = 10_000, examples = ["Buy milk, eggs, and bread"])

class NoteResponse(BM):
    id: str
    title: str | None
    content: str
    created_at: date

    model_config = {"from_attributes": True}

class ErrorDetail(BM):
    detail: str