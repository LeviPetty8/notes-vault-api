"""API-level integration tests — each test gets a fresh in-memory database."""


def test_create_note_returns_201(client):
    resp = client.post("/notes", json={"content": "Hello, world!"})
    assert resp.status_code == 201
    body = resp.json()
    assert body["content"] == "Hello, world!"
    assert "id" in body
    assert "created_at" in body
    assert body["title"] is None


def test_create_note_with_title(client):
    resp = client.post("/notes", json={"title": "My title", "content": "Some content"})
    assert resp.status_code == 201
    assert resp.json()["title"] == "My title"


def test_create_note_empty_content_is_rejected(client):
    resp = client.post("/notes", json={"content": ""})
    assert resp.status_code == 422


def test_create_note_missing_content_is_rejected(client):
    resp = client.post("/notes", json={"title": "No content"})
    assert resp.status_code == 422


def test_create_note_content_too_long_is_rejected(client):
    resp = client.post("/notes", json={"content": "x" * 10_001})
    assert resp.status_code == 422


def test_list_notes_empty(client):
    resp = client.get("/notes")
    assert resp.status_code == 200
    assert resp.json() == []


def test_list_notes_returns_all(client):
    client.post("/notes", json={"content": "First"})
    client.post("/notes", json={"content": "Second"})
    resp = client.get("/notes")
    assert resp.status_code == 200
    assert len(resp.json()) == 2


def test_list_notes_ordered_newest_first(client):
    client.post("/notes", json={"content": "Older"})
    client.post("/notes", json={"content": "Newer"})
    notes = client.get("/notes").json()
    assert notes[0]["content"] == "Newer"


def test_get_note_by_id(client):
    note_id = client.post("/notes", json={"content": "Find me"}).json()["id"]
    resp = client.get(f"/notes/{note_id}")
    assert resp.status_code == 200
    assert resp.json()["content"] == "Find me"


def test_get_note_not_found(client):
    resp = client.get("/notes/does-not-exist")
    assert resp.status_code == 404
    assert "detail" in resp.json()


def test_delete_note_returns_204(client):
    note_id = client.post("/notes", json={"content": "Delete me"}).json()["id"]
    resp = client.delete(f"/notes/{note_id}")
    assert resp.status_code == 204


def test_deleted_note_is_gone(client):
    note_id = client.post("/notes", json={"content": "Gone soon"}).json()["id"]
    client.delete(f"/notes/{note_id}")
    assert client.get(f"/notes/{note_id}").status_code == 404
    assert len(client.get("/notes").json()) == 0


def test_delete_note_not_found(client):
    resp = client.delete("/notes/does-not-exist")
    assert resp.status_code == 404
    assert "detail" in resp.json()
