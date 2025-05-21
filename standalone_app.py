#!/usr/bin/env python
"""
Standalone FastAPI application for testing.
"""

from fastapi import FastAPI, APIRouter
import uvicorn

app = FastAPI(
    title="Test FastAPI App",
    description="A test application",
    version="0.1.0",
)

router = APIRouter()


@router.get("/health")
async def health_check():
    """Basic health check endpoint."""
    return {"status": "ok", "message": "Service is healthy"}


app.include_router(router, prefix="/api/v1")


@app.get("/")
async def root():
    """Root endpoint."""
    return {"message": "Welcome to the test API"}


if __name__ == "__main__":
    uvicorn.run("standalone_app:app", host="127.0.0.1", port=8001, reload=True)
