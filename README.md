# Notes Vault API

A small REST API for creating, viewing, and deleting notes. Built with Python, FastAPI, and SQLite.

---

## System Overview

A single-process HTTP service that exposes four REST endpoints. Notes are stored in a local SQLite file (`notes.db`) that is created automatically on first run. The server auto-generates interactive API docs at `http://localhost:3000/docs` (Swagger UI) and `http://localhost:3000/redoc`.

---

## Tech Choices

| Layer | Choice | Reason |
|---|---|---|
| Language | Python 3.11+ | Readable, fast to iterate, rich ecosystem |
| Framework | FastAPI | Automatic request validation via Pydantic, built-in OpenAPI docs, async-ready |
| ORM | SQLAlchemy 2.x | Thin, explicit, easy migration to any RDBMS |
| Database | SQLite | Zero-infrastructure persistence, ships with Python |
| Tests | pytest + httpx | `TestClient` drives real HTTP through the full stack; clean fixtures |

### SQLite Over In-Memory Storage

SQLite gives real persistence with no infrastructure to install. Notes survive server restarts without any extra work.

---

## Project Structure

```
.
├── app/
│   ├── database.py   # SQLAlchemy engine, session factory, get_db dependency
│   ├── models.py     # Note ORM model
│   ├── schemas.py    # Pydantic request/response schemas
│   └── main.py       # FastAPI app and route handlers
├── tests/
│   ├── conftest.py   # Shared fixtures (in-memory test DB, TestClient)
│   ├── test_api.py   # API-level integration tests
│   └── test_data.py  # Data-layer / ORM unit tests
├── run.py            # Entrypoint — starts uvicorn
├── start.sh          # Single-command launcher (Linux/macOS)
├── start.bat         # Single-command launcher (Windows)
└── requirements.txt
```

---

## Running the Project

**Prerequisite:** Python 3.11+ installed and available as `python` (or `python3`).

### Single Command

**Windows:**
```
.\start.bat
```

**Linux / macOS:**
```bash
chmod +x start.sh && ./start.sh
```

Both scripts install dependencies and start the server. The API is then available at `http://localhost:3000`.

### Manual Steps (Optional)

```bash
pip install -r requirements.txt
python run.py
```

---

## Running Tests

```bash
pip install -r requirements.txt
python -m pytest tests/ -v
```

Tests use an isolated in-memory SQLite database. They never touch `notes.db` and can be run while the server is running.

---

## API Reference

### Data Model

| Field | Type | Description |
|---|---|---|
| `id` | string (UUID) | Auto-generated unique identifier
| `title` | string \| null | Optional, max 200 characters |
| `content` | string | Required, 1-10,000 characters |
| `created_at` | ISO 8601 datetime | Set automatically on creation |

### Endpoints

#### `POST /notes` - Create a note

**Request body:**
```json
{
    "title": "Optional title",
    "content": "Note content (required)"
}
```

**Responses:**
- `201 Created` - Note created; returns the full note object
- `422 Unprocessable entity` - Validation failed (e.g. empty content)

```bash
curl -s -X POST http://localhost:3000/notes \
  -H "Content-Type: application/json" \
  -d '{"title": "Groceries", "content": "Milk, eggs, bread"}'
```

```json
{
    "id": "16f5e63b-...",
    "title": "Groceries",
    "content": "Milk, eggs, bread",
    "created_at": "2026-05-07T16:40:52.678074"
}
```

---

#### `GET /notes` - List all notes

Returns all notes ordered newest-first.

**Responses:**
- `200 OK` - Array of note objects (empty array if none exist)

```bash
curl -s http://localhost:3000/notes
```

OR

```bash
curl -s -X GET http://localhost:3000/notes
```

---

#### `GET /notes/{id}` - Get a note by ID

**Responses:**
- `200 OK` - The note object
- `404 Not Found` - Note with that ID does not exist

```bash
curl -s http://localhost:3000/notes/{id}
```

OR

```bash
curl -s -X GET http://localhost:3000/notes/{id}
```

---

#### `DELETE /notes/{id}` - Delete a note by ID

**Responses:**
- `204 No Content` - Note deleted
- `404 Not Found` - Note with that ID does not exist

```bash
curl -s -X DELETE http://localhost:3000/notes/{id}
# No response body on success
```

---

### Error Response Shape

All error responses use a consistent JSON envelope:

```json
{
    "detail": "Note '...' not found"
}
```

Validation errors from Pydantic follow FastAPI's standard 422 shape with a `detail` array.

---

## Assumptions and Trade-Offs

**UUID strings as IDs.** Using string UUIDs rather than auto-increment integers avoids exposing record counts and makes IDs safe to generate client-side. The trade-off is slightly larger storage and no natural ordering by ID.

**No pagination on `GET /notes`.** For a small notes service this is fine. At scale, offset/cursor pagination would be needed.

**No authentication.**

**Content length capped at 10,000 characters.** Prevents accidentally huge payloads from being stored. The value is arbitrary and easy to change in `schemas.py`.

---

## Potential Future Improvements

- `PATCH /notes/{id}` - Update title or content of an existing note
- `GET /notes?q=...` - Full-text search using SQLite
- Pagination: `?limit=20&offset=0` query parameters
- Authentication

