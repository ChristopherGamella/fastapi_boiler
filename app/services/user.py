import secrets
from datetime import datetime, timedelta
from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import get_password_hash
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate


async def get_user_by_username(db: AsyncSession, username: str) -> Optional[User]:
    """Get a user by username."""
    result = await db.execute(select(User).where(User.username == username))
    return result.scalars().first()


async def get_user_by_email(db: AsyncSession, email: str) -> Optional[User]:
    """Get a user by email."""
    result = await db.execute(select(User).where(User.email == email))
    return result.scalars().first()


async def get_user_by_id(db: AsyncSession, user_id: int) -> Optional[User]:
    """Get a user by ID."""
    result = await db.execute(select(User).where(User.id == user_id))
    return result.scalars().first()


async def get_users(db: AsyncSession, skip: int = 0, limit: int = 100) -> List[User]:
    """Get all users."""
    result = await db.execute(select(User).offset(skip).limit(limit))
    return result.scalars().all()


async def create_user(db: AsyncSession, user_in: UserCreate) -> User:
    """Create a new user."""
    # Check if username or email already exists
    existing_user = await get_user_by_username(db, username=user_in.username)
    if existing_user:
        raise ValueError("Username already registered")
        
    existing_email = await get_user_by_email(db, email=user_in.email)
    if existing_email:
        raise ValueError("Email already registered")
    
    # Create new user
    user = User(
        username=user_in.username,
        email=user_in.email,
        full_name=user_in.full_name,
        hashed_password=get_password_hash(user_in.password),
        is_active=user_in.is_active,
    )
    
    db.add(user)
    await db.commit()
    await db.refresh(user)
    
    return user


async def update_user(
    db: AsyncSession, user: User, user_in: UserUpdate
) -> User:
    """Update a user."""
    # Update attributes
    if user_in.username is not None:
        user.username = user_in.username
    if user_in.email is not None:
        user.email = user_in.email
    if user_in.full_name is not None:
        user.full_name = user_in.full_name
    if user_in.password is not None:
        user.hashed_password = get_password_hash(user_in.password)
    if user_in.is_active is not None:
        user.is_active = user_in.is_active
        
    db.add(user)
    await db.commit()
    await db.refresh(user)
    
    return user


async def delete_user(db: AsyncSession, user_id: int) -> None:
    """Delete a user."""
    user = await get_user_by_id(db, user_id=user_id)
    if user:
        await db.delete(user)
        await db.commit()


async def set_password_reset_token(db: AsyncSession, email: str) -> Optional[User]:
    """Set password reset token for a user."""
    user = await get_user_by_email(db, email=email)
    if not user:
        return None

    # Generate a secure token and set expiration time (24 hours)
    reset_token = secrets.token_urlsafe(32)
    reset_expires = datetime.utcnow() + timedelta(hours=24)
    
    # Update user with reset token info
    user.password_reset_token = reset_token
    user.password_reset_expires = reset_expires
    
    db.add(user)
    await db.commit()
    await db.refresh(user)
    
    return user


async def verify_password_reset_token(db: AsyncSession, token: str) -> Optional[User]:
    """Verify a password reset token."""
    # Find user with this token
    result = await db.execute(select(User).where(User.password_reset_token == token))
    user = result.scalars().first()
    
    if not user:
        return None
        
    # Check if token has expired
    if user.password_reset_expires < datetime.utcnow():
        return None
        
    return user


async def reset_password_with_token(db: AsyncSession, token: str, new_password: str) -> Optional[User]:
    """Reset a user's password with a valid token."""
    user = await verify_password_reset_token(db, token)
    if not user:
        return None
        
    # Update password and clear reset token
    user.hashed_password = get_password_hash(new_password)
    user.password_reset_token = None
    user.password_reset_expires = None
    
    db.add(user)
    await db.commit()
    await db.refresh(user)
    
    return user
