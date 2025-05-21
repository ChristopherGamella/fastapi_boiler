import logging

from app.db.session import engine
from app.models.base import Base

logger = logging.getLogger(__name__)


async def connect_to_db() -> None:
    """
    Create database tables on startup if they don't exist.
    
    In production, you should use Alembic instead of this approach.
    """
    logger.info("Connecting to database")
    
    try:
        # Create tables
        async with engine.begin() as conn:
            # Only create tables in development mode
            from app.core.config import settings
            if settings.ENV == "development":
                logger.info("Creating database tables")
                await conn.run_sync(Base.metadata.create_all)
                
        logger.info("Connected to database")
    except Exception as e:
        logger.error(f"Error connecting to database: {e}")
        raise


async def close_db_connection() -> None:
    """Close database connection on shutdown."""
    logger.info("Closing database connection")
    
    try:
        await engine.dispose()
        logger.info("Database connection closed")
    except Exception as e:
        logger.error(f"Error closing database connection: {e}")
        raise
