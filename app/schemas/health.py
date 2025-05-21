from typing import Dict, Any
from pydantic import BaseModel


class HealthCheck(BaseModel):
    """Schema for basic health check response."""
    
    status: str
    message: str


class HealthDetail(BaseModel):
    """Schema for detailed health check response."""
    
    status: str
    message: str
    details: Dict[str, Dict[str, Any]]
