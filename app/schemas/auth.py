from pydantic import BaseModel


class Token(BaseModel):
    """Schema for JWT token."""
    
    access_token: str
    token_type: str


class TokenData(BaseModel):
    """Schema for JWT token payload."""
    
    username: str
