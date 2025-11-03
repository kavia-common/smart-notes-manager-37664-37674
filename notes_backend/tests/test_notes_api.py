from fastapi.testclient import TestClient

# Import the FastAPI app from the local package using a relative import
from ..src.api.main import app  # type: ignore

client = TestClient(app)


def test_health():
    r = client.get("/")
    assert r.status_code == 200
    assert r.json()["message"] == "Healthy"


def test_crud_flow():
    # Create
    payload = {"title": "Test", "content": "Body", "tags": ["a", "b"]}
    r = client.post("/notes", json=payload)
    assert r.status_code == 201
    note = r.json()
    note_id = note["id"]

    # Get
    r = client.get(f"/notes/{note_id}")
    assert r.status_code == 200
    assert r.json()["title"] == "Test"

    # Update
    upd = {"content": "Updated"}
    r = client.put(f"/notes/{note_id}", json=upd)
    assert r.status_code == 200
    assert r.json()["content"] == "Updated"

    # Archive
    r = client.patch(f"/notes/{note_id}/archive", params={"archived": True})
    assert r.status_code == 200
    assert r.json()["archived"] is True

    # Search
    r = client.get("/notes/search", params={"q": "Updated"})
    assert r.status_code == 200
    assert len(r.json()) >= 1

    # Delete
    r = client.delete(f"/notes/{note_id}")
    assert r.status_code == 204

    # Not found afterwards
    r = client.get(f"/notes/{note_id}")
    assert r.status_code == 404
