from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.api.v1.api import api_router
from app.core.config import settings
from app.db.events import close_db_connection, connect_to_db


def create_app() -> FastAPI:
    """Create FastAPI application."""
    description = settings.DESCRIPTION

    app = FastAPI(
        title=settings.PROJECT_NAME,
        description=description,
        version=settings.VERSION,
        docs_url="/docs",
        redoc_url="/redoc",
    )

    # Set up CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Include API router
    app.include_router(api_router, prefix=settings.API_V1_PREFIX)

    # Root endpoint
    @app.get("/", tags=["Root"])
    async def root():
        return JSONResponse(
            content={
                "message": f"Welcome to {settings.PROJECT_NAME} API",
                "version": settings.VERSION,
                "docs_url": "/docs",
            }
        )

    # Add event handlers
    app.add_event_handler("startup", connect_to_db)
    app.add_event_handler("shutdown", close_db_connection)

    return app
