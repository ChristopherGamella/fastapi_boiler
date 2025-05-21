# Database models import
from app.models.base import Base
from app.models.user import User

# This import is needed by Alembic to discover all database models
# Add all models to be discovered by Alembic

__all__ = ["Base", "User"]
