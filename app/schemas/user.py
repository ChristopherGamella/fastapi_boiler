from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field


# Shared properties
class UserBase(BaseModel):
    """Base user schema."""
    
    username: str
    email: EmailStr
    full_name: Optional[str] = None
    is_active: bool = True


# Properties to receive on user creation
class UserCreate(UserBase):
    """Schema for creating a user."""
    
    password: str = Field(..., min_length=8)


# Properties to receive on user update
class UserUpdate(BaseModel):
    """Schema for updating a user."""
    
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    password: Optional[str] = Field(None, min_length=8)
    is_active: Optional[bool] = None


# Additional properties stored in DB
class UserInDB(UserBase):
    """Schema representing a user in the database."""
    
    id: int
    hashed_password: str
    is_superuser: bool = False
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# Additional properties to return via API
class User(UserBase):
    """Schema for returning a user."""
    id: int
    is_superuser: bool = False
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
    
    id: int
    is_superuser: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
