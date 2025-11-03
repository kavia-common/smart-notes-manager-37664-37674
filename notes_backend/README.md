# Smart Notes Manager - Notes Backend

FastAPI backend for a notes application. Provides CRUD operations, search and tag filtering, and archive/unarchive.

## Features

- FastAPI with OpenAPI/Swagger docs
- Endpoints:
  - GET `/` health check
  - POST `/notes`
  - GET `/notes`
  - GET `/notes/{id}`
  - PUT `/notes/{id}`
  - DELETE `/notes/{id}`
  - PATCH `/notes/{id}/archive?archived=true|false`
  - GET `/notes/search?q=...&tag=...&archived=true|false`
- In-memory storage (no external DB required)
- CORS enabled for all origins
- UUID-based IDs and UTC timestamps

## Running locally

The live preview expects the app on port `3001`.

Using uvicorn:

```
uvicorn smart-notes-manager-37664-37674.notes_backend.src.api.main:app --host 0.0.0.0 --port 3001
```

Swagger UI: `http://localhost:3001/docs`  
OpenAPI JSON: `http://localhost:3001/openapi.json`

## Request/Response Schemas

- NoteCreate
  - title: string (required, 1..256)
  - content: string
  - tags: string[]
  - archived: boolean (default: false)

- NoteUpdate (partial)
  - title?: string
  - content?: string
  - tags?: string[]
  - archived?: boolean

- NoteOut
  - id: UUID
  - title: string
  - content: string
  - tags: string[]
  - created_at: ISO datetime (UTC)
  - updated_at: ISO datetime (UTC)
  - archived: boolean

## Example Usage

Create a note:

```
curl -X POST http://localhost:3001/notes \
  -H "Content-Type: application/json" \
  -d '{"title":"Groceries","content":"Buy milk and eggs","tags":["home","errands"]}'
```

List notes:

```
curl http://localhost:3001/notes
```

Get a note:

```
curl http://localhost:3001/notes/{id}
```

Update a note:

```
curl -X PUT http://localhost:3001/notes/{id} \
  -H "Content-Type: application/json" \
  -d '{"content":"Buy milk, eggs, and bread"}'
```

Delete a note:

```
curl -X DELETE http://localhost:3001/notes/{id}
```

Archive a note:

```
curl -X PATCH "http://localhost:3001/notes/{id}/archive?archived=true"
```

Search:

```
curl "http://localhost:3001/notes/search?q=milk&tag=home&archived=false"
```

## Testing

You can add minimal tests using pytest later; the repository supports easy unit testing of the in-memory layer and routes.

## Environment

No environment variables are required. See `.env.example` for future options.
