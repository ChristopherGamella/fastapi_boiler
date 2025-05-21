from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.db.session import get_db
from app.schemas.health import HealthCheck, HealthDetail

router = APIRouter()


@router.get("", response_model=HealthCheck)
async def health_check():
    """Basic health check."""
    return {"status": "ok", "message": "Service is healthy"}


@router.get("/details", response_model=HealthDetail)
async def health_check_details(db: AsyncSession = Depends(get_db)):
    """Detailed health check including database connection."""
    db_status = "ok"
    db_message = "Database connection successful"
    
    try:
        # Execute a simple query to check database connectivity
        await db.execute(select(1))
    except Exception as e:
        db_status = "error"
        db_message = f"Database connection failed: {str(e)}"
        
    return {
        "status": "ok" if db_status == "ok" else "error",
        "message": "Service health details",
        "details": {
            "database": {
                "status": db_status,
                "message": db_message
            },
            "api": {
                "status": "ok",
                "version": "0.1.0"
            }
        }
    }
