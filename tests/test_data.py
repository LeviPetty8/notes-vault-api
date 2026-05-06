"""Data-layer tests — exercise the ORM model directly, no HTTP involved."""
import uuid
from datetime import datetime as date, timezone as zone

from app.models import Note


def test_note_persists_and_is_queryable(db_session):
    note = Note(id=str(uuid.uuid4()), content="Persisted note")
    db_session.add(note)
    db_session.commit()

    result = db_session.query(Note).filter(Note.id == note.id).first()
    assert result is not None
    assert result.content == "Persisted note"


def test_note_created_at_is_set_automatically(db_session):
    note = Note(id=str(uuid.uuid4()), content="Timestamped")
    db_session.add(note)
    db_session.commit()
    db_session.refresh(note)

    assert note.created_at is not None
    assert isinstance(note.created_at, date)


def test_note_title_is_optional(db_session):
    note = Note(id=str(uuid.uuid4()), content="No title")
    db_session.add(note)
    db_session.commit()
    db_session.refresh(note)

    assert note.title is None


def test_multiple_notes_are_stored_independently(db_session):
    ids = [str(uuid.uuid4()) for _ in range(3)]
    for i, nid in enumerate(ids):
        db_session.add(Note(id=nid, content=f"Note {i}"))
    db_session.commit()

    assert db_session.query(Note).count() == 3


def test_delete_removes_note_from_database(db_session):
    note = Note(id=str(uuid.uuid4()), content="To be deleted")
    db_session.add(note)
    db_session.commit()

    db_session.delete(note)
    db_session.commit()

    assert db_session.query(Note).filter(Note.id == note.id).first() is None


def test_ids_are_unique_per_note(db_session):
    notes = [Note(id=str(uuid.uuid4()), content=f"Note {i}") for i in range(5)]
    for n in notes:
        db_session.add(n)
    db_session.commit()

    stored_ids = {n.id for n in db_session.query(Note).all()}
    assert len(stored_ids) == 5
