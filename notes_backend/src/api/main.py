from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routers.notes import router as notes_router

# PUBLIC_INTERFACE
def create_app() -> FastAPI:
    """
    Create and configure the FastAPI application with CORS, metadata, and routes.

    Returns:
        FastAPI: Configured FastAPI app instance.
    """
    app = FastAPI(
        title="Smart Notes Manager - Notes API",
        description=(
            "A simple Notes API supporting CRUD operations, search/filtering, and archive/unarchive functionality. "
            "Designed with clean architecture and in-memory storage by default."
        ),
        version="0.1.0",
        openapi_tags=[
            {
                "name": "health",
                "description": "Service health and readiness endpoints",
            },
            {
                "name": "notes",
                "description": "Notes CRUD, search, and archive operations",
            },
        ],
    )

    # Enable permissive CORS (can be restricted later)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.get("/", summary="Health Check", tags=["health"])
    def health_check():
        """
        Health check endpoint.

        Returns:
            dict: A simple message indicating service is healthy.
        """
        return {"message": "Healthy"}

    # Register notes API router
    app.include_router(notes_router, prefix="/notes", tags=["notes"])

    return app


app = create_app()

# For local execution: uvicorn smart-notes-manager-37664-37674.notes_backend.src.api.main:app --host 0.0.0.0 --port 3001
