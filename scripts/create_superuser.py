"""Script to create a superuser in the database."""

import asyncio
import logging
import os
import sys
from pathlib import Path
from pydantic_settings import BaseSettings

# Add the parent directory to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.db.session import SessionLocal
from app.models.user import User
from app.core.security import get_password_hash


class SuperUserSettings(BaseSettings):
    """Settings for the superuser."""
    
    SUPERUSER_USERNAME: str = "admin"
    SUPERUSER_EMAIL: str = "admin@example.com"
    SUPERUSER_PASSWORD: str = "adminpassword"
    SUPERUSER_FULL_NAME: str = "Administrator"


async def create_superuser() -> None:
    """Create a superuser in the database."""
    settings = SuperUserSettings()
    
    async with SessionLocal() as db:
        # Check if superuser already exists
        result = await db.execute(User.__table__.select().where(User.username == settings.SUPERUSER_USERNAME))
        user = result.scalars().first()
        
        if user:
            logging.info(f"Superuser {settings.SUPERUSER_USERNAME} already exists")
            return
            
        # Create superuser
        superuser = User(
            username=settings.SUPERUSER_USERNAME,
            email=settings.SUPERUSER_EMAIL,
            full_name=settings.SUPERUSER_FULL_NAME,
            hashed_password=get_password_hash(settings.SUPERUSER_PASSWORD),
            is_active=True,
            is_superuser=True,
        )
        
        db.add(superuser)
        await db.commit()
        
        logging.info(f"Superuser {settings.SUPERUSER_USERNAME} created successfully")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(create_superuser())
