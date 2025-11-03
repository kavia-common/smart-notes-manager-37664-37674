# smart-notes-manager-37664-37674

This workspace contains the Notes Backend (FastAPI) for Smart Notes Manager.

- Backend container: `notes_backend`
- Framework: FastAPI
- API Docs (when running): http://localhost:3001/docs

To run the backend locally:

1. Install dependencies (already listed in `notes_backend/requirements.txt`).
2. Start the server on port 3001:

```
uvicorn smart-notes-manager-37664-37674.notes_backend.src.api.main:app --host 0.0.0.0 --port 3001
```

For detailed API usage, see `notes_backend/README.md`.
