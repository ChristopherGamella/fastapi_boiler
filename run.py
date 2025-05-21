#!/usr/bin/env python
"""
Run script to start the FastAPI application with uvicorn.
"""

import argparse
import uvicorn

from app.core.config import settings

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="FastAPI Boilerplate")
    parser.add_argument("--host", help="Host to bind", default=settings.HOST)
    parser.add_argument("--port", type=int, help="Port to bind", default=settings.PORT)
    parser.add_argument("--reload", action="store_true", help="Enable auto-reload")
    args = parser.parse_args()

    uvicorn.run(
        "main:app",
        host=args.host,
        port=args.port,
        reload=args.reload or settings.ENV == "development",
        log_level=settings.LOG_LEVEL.lower(),
    )
