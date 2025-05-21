from fastapi import FastAPI
from fastapi.testclient import TestClient
import pytest
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from app.core.app_factory import create_app
from app.core.config import settings
from app.db.session import get_db
from app.models.base import Base

# Use an in-memory SQLite database for testing
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

# Override settings for testing
settings.DATABASE_URL = TEST_DATABASE_URL
settings.ENV = "testing"


@pytest.fixture
def app() -> FastAPI:
    """Create a FastAPI test application."""
    return create_app()


@pytest.fixture
def client(app: FastAPI) -> TestClient:
    """Create a FastAPI test client."""
    return TestClient(app)


@pytest.fixture
async def async_test_engine():
    """Create an async SQLite engine for tests."""
    engine = create_async_engine(TEST_DATABASE_URL, echo=False)
    
    # Create all tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    
    yield engine
    
    # Dispose of the engine after tests
    await engine.dispose()


@pytest.fixture
async def db_session(async_test_engine):
    """Create a test database session."""
    # Create session factory
    test_session_maker = sessionmaker(
        bind=async_test_engine, 
        class_=AsyncSession, 
        expire_on_commit=False,
        autoflush=False,
    )
    
    # Create a new session for the test
    async with test_session_maker() as session:
        yield session


# Override the get_db dependency for testing
@pytest.fixture
def override_get_db(db_session):
    """Override the get_db dependency for testing."""
    
    async def _override_get_db():
        yield db_session
    
    return _override_get_db
