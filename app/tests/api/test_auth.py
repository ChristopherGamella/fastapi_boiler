import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.security import create_access_token
from app.db.session import get_db
from app.services.user import create_user
from app.schemas.user import UserCreate


@pytest.fixture
async def test_user(db_session: AsyncSession):
    """Create a test user."""
    user_in = UserCreate(
        username="testuser",
        email="test@example.com",
        password="testpassword",
        full_name="Test User"
    )
    user = await create_user(db=db_session, user_in=user_in)
    return user


@pytest.mark.asyncio
async def test_get_access_token(
    client: TestClient, 
    app: FastAPI, 
    override_get_db, 
    test_user
):
    """Test getting an access token."""
    # Override get_db to use test database
    app.dependency_overrides[get_db] = override_get_db
    
    # Get access token
    login_data = {
        "username": "testuser",
        "password": "testpassword",
    }
    response = client.post("/api/v1/auth/token", data=login_data)
    
    # Test response
    assert response.status_code == 200
    token = response.json()
    assert "access_token" in token
    assert token["token_type"] == "bearer"


@pytest.mark.asyncio
async def test_get_current_user(
    client: TestClient, 
    app: FastAPI, 
    override_get_db, 
    test_user
):
    """Test getting the current user."""
    # Override get_db to use test database
    app.dependency_overrides[get_db] = override_get_db
    
    # Create access token
    access_token = create_access_token(data={"sub": test_user.username})
    
    # Get current user
    headers = {"Authorization": f"Bearer {access_token}"}
    response = client.get("/api/v1/auth/me", headers=headers)
    
    # Test response
    assert response.status_code == 200
    user_data = response.json()
    assert user_data["username"] == test_user.username
    assert user_data["email"] == test_user.email
