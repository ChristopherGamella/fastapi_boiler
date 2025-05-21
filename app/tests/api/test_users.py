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


@pytest.fixture
async def test_superuser(db_session: AsyncSession):
    """Create a test superuser."""
    user_in = UserCreate(
        username="admin",
        email="admin@example.com",
        password="adminpassword",
        full_name="Admin User"
    )
    user = await create_user(db=db_session, user_in=user_in)
    # Make user a superuser
    user.is_superuser = True
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)
    return user


@pytest.fixture
def user_token(test_user):
    """Create a token for a test user."""
    return create_access_token(data={"sub": test_user.username})


@pytest.fixture
def superuser_token(test_superuser):
    """Create a token for a test superuser."""
    return create_access_token(data={"sub": test_superuser.username})


@pytest.mark.asyncio
async def test_create_user(
    client: TestClient, 
    app: FastAPI, 
    override_get_db
):
    """Test creating a new user."""
    # Override get_db to use test database
    app.dependency_overrides[get_db] = override_get_db
    
    # Create user
    user_data = {
        "username": "newuser",
        "email": "newuser@example.com",
        "password": "newuserpassword",
        "full_name": "New User"
    }
    response = client.post("/api/v1/users", json=user_data)
    
    # Test response
    assert response.status_code == 201
    created_user = response.json()
    assert created_user["username"] == user_data["username"]
    assert created_user["email"] == user_data["email"]
    assert "id" in created_user
    assert "password" not in created_user


@pytest.mark.asyncio
async def test_get_users(
    client: TestClient, 
    app: FastAPI, 
    override_get_db,
    test_user,
    user_token
):
    """Test getting all users."""
    # Override get_db to use test database
    app.dependency_overrides[get_db] = override_get_db
    
    # Get users
    headers = {"Authorization": f"Bearer {user_token}"}
    response = client.get("/api/v1/users", headers=headers)
    
    # Test response
    assert response.status_code == 200
    users = response.json()
    assert isinstance(users, list)
    assert len(users) >= 1


@pytest.mark.asyncio
async def test_get_user_by_id(
    client: TestClient, 
    app: FastAPI, 
    override_get_db,
    test_user,
    user_token
):
    """Test getting a user by ID."""
    # Override get_db to use test database
    app.dependency_overrides[get_db] = override_get_db
    
    # Get user
    headers = {"Authorization": f"Bearer {user_token}"}
    response = client.get(f"/api/v1/users/{test_user.id}", headers=headers)
    
    # Test response
    assert response.status_code == 200
    user_data = response.json()
    assert user_data["id"] == test_user.id
    assert user_data["username"] == test_user.username
    assert user_data["email"] == test_user.email
