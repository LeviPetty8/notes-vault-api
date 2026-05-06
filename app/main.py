import uuid
from datetime import datetime as date, timezone as zone

from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy.orm import Session

from app import models, schemas
from app.database import Base, engine, get_db

Base.metadata.create_all(bind = engine)

app = FastAPI(
    title = "Notes Vault API",
    version = "1.0.0",
    description = "A simple REST API for creating, viewing, and deleting notes."
)

@app.post(
    "/notes",
    response_model = schemas.NoteResponse,
    status_code = status.HTTP_201_CREATED
    summary = "Create a note"
)
def create_note(payload: schemas.NoteCreate, db: Session = Depends(get_db)):
    note = models.Note(
        id = str(uuid.uuid4()),
        title = payload.title,
        content = payload.content,
        created_at = date.now(zone.utc)
    )
    db.add(note)
    db.commit()
    db.refresh(note)
    return note

@app.get(
    "/notes/{note_id}",
    response_model = schemas.NoteResponse,
    responses = {404: {"model": schemas.ErrorDetail}},
    summary = "Get a note by ID"
)
def get_note(note_id: str, db: Session = Depends(get_db)):
    note = db.query(models.Note).filter(models.Note.id == note_id).first()
    if not note:
        raise HTTPException(status_code = 404, detail = f"Note '{note_id}' not found")
    return note

@app.delete(
    "/notes/{note_id}",
    status_code = status.HTTP_204_NO_CONTENT,
    responses = {404: {"model": schemas.ErrorDetail}},
    summary = "Delete a note by ID"
)
def delete_note(note_id: str, db: Session = Depends(get_db)):
    note = db.query(models.Note).filter(models.Note.id == note_id).first()
    if not note:
        raise HTTPException(status_code = 404, detail = f"Note '{note_id}' not found")
    db.delete(note)
    db.commit()