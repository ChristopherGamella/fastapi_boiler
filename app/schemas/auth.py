from pydantic import BaseModel, EmailStr, Field


class Token(BaseModel):
    """Schema for JWT token."""
    
    access_token: str
    token_type: str


class TokenData(BaseModel):
    """Schema for JWT token payload."""
    
    username: str


class PasswordForgotRequest(BaseModel):
    """Schema for forgot password request."""
    
    email: EmailStr


class PasswordForgotResponse(BaseModel):
    """Schema for forgot password response."""
    
    message: str


class PasswordResetRequest(BaseModel):
    """Schema for reset password request."""
    
    token: str
    password: str = Field(..., min_length=8)


class PasswordResetResponse(BaseModel):
    """Schema for reset password response."""
    
    message: str
