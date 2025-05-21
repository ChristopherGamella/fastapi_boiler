from fastapi import APIRouter

from app.api.v1.endpoints import auth, users, health

api_router = APIRouter()

# Include endpoints
api_router.include_router(health.router, prefix="/health", tags=["Health"])
api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(users.router, prefix="/users", tags=["Users"])
