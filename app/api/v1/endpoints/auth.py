from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import create_access_token
from app.db.session import get_db
from app.schemas.auth import (
    PasswordForgotRequest, 
    PasswordForgotResponse, 
    PasswordResetRequest, 
    PasswordResetResponse, 
    Token
)
from app.schemas.user import User
from app.services.auth import authenticate_user, get_current_user
from app.services.user import (
    get_user_by_email,
    reset_password_with_token,
    set_password_reset_token
)

router = APIRouter()


@router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db),
):
    """Authenticate user and return JWT token."""
    user = await authenticate_user(form_data.username, form_data.password, db=db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_user)):
    """Get current authenticated user."""
    return current_user


@router.post("/forgot-password", response_model=PasswordForgotResponse)
async def forgot_password(
    request: PasswordForgotRequest,
    db: AsyncSession = Depends(get_db),
):
    """Request password reset."""
    # Check if user exists with given email
    user = await get_user_by_email(db, email=request.email)
    
    # Always return a generic message to prevent email enumeration attacks
    if not user:
        return {"message": "If your email is registered, you will receive a password reset link."}
    
    # Generate reset token and set expiry
    user = await set_password_reset_token(db, email=request.email)
    
    # In a real application, you would send an email with the reset link here
    # For now, we'll just return the token in the response (for development/testing only)
    reset_token = user.password_reset_token
    
    # In production, you should not include the token in the response
    # This is just for development convenience
    return {"message": f"Password reset link sent. Token: {reset_token}"}


@router.post("/reset-password", response_model=PasswordResetResponse)
async def reset_password(
    request: PasswordResetRequest,
    db: AsyncSession = Depends(get_db),
):
    """Reset password using reset token."""
    user = await reset_password_with_token(db, token=request.token, new_password=request.password)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired password reset token",
        )
    
    return {"message": "Password has been reset successfully"}
