from pydantic import EmailStr
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.identity_service.app.services.auth_service import (
    refresh_access_token,
    verify_email,
    request_password_reset,
    reset_password,
    logout_user
)
from src.common.db.database import get_db
from src.common.dependencies.user_data import get_current_user

from src.identity_service.app.repositories.user import (
    create_user,
    authenticate_user
)
from src.identity_service.app.models.user import User
from src.identity_service.app.schemas.token import Token
from src.identity_service.app.schemas.user import (
    UserCreate,
    UserLogin,
    UserResponse
)
from src.identity_service.app.utils.security import create_access_token

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/sign-up", response_model=Token, status_code=status.HTTP_201_CREATED)
async def sign_up(user_in: UserCreate, db: AsyncSession = Depends(get_db)):
    """
    Register a new user.

    Args:
        user_in (UserCreate): User registration details
        db (AsyncSession): Database session

    Returns:
        Token: Access token for the new user
    """
    try:
        # Create user
        new_user = await create_user(db, user_in)

        # Generate access token
        access_token = create_access_token(
            data={"id": new_user.id, "email": new_user.email}
        )

        return Token(access_token=access_token, token_type="bearer")

    except HTTPException as e:
        raise e


@router.post("/sign-in", response_model=Token)
async def sign_in(user_in: UserLogin, db: AsyncSession = Depends(get_db)):
    """
    Authenticate user and generate tokens.

    Args:
        user_in (UserLogin): User login credentials
        db (AsyncSession): Database session

    Returns:
        Token: Access and refresh tokens
    """
    # Authenticate user
    user = await authenticate_user(db, user_in)

    # Generate tokens
    access_token = create_access_token(
        data={"id": user.id, "email": user.email}
    )
    refresh_token = create_access_token(
        data={"id": user.id, "email": user.email}
    )

    return Token(access_token=access_token, refresh_token=refresh_token)


@router.get("/me", response_model=UserResponse)
async def read_current_user(current_user: User = Depends(get_current_user)):
    """
    Retrieve current user's profile.

    Args:
        current_user (User): Authenticated user

    Returns:
        UserResponse: User profile information
    """
    return UserResponse.model_validate(current_user)


@router.post("/refresh-token", response_model=Token)
async def refresh_token(refresh_token: str, db: AsyncSession = Depends(get_db)):
    """
    Generate new access token using refresh token.

    Args:
        refresh_token (str): Refresh token
        db (AsyncSession): Database session

    Returns:
        Token: New access token
    """
    return await refresh_access_token(db, refresh_token)


@router.post("/verify-email", response_model=dict)
async def verify_email_route(email: str, code: str, db: AsyncSession = Depends(get_db)):
    """
    Verify user's email address.

    Args:
        email (str): User's email
        code (str): Verification code
        db (AsyncSession): Database session

    Returns:
        dict: Verification status
    """
    await verify_email(db, email, code)
    return {"message": "Email confirmed successfully"}


@router.post("/forgot-password", response_model=dict)
async def forgot_password(email: EmailStr, db: AsyncSession = Depends(get_db)):
    """
    Initiate password reset process.

    Args:
        email (EmailStr): User's email
        db (AsyncSession): Database session

    Returns:
        dict: Password reset request status
    """
    return await request_password_reset(db, email)


@router.post("/reset-password", response_model=dict)
async def reset_password_route(email: str, code: str, new_password: str, db: AsyncSession = Depends(get_db)):
    """
    Reset user's password.

    Args:
        email (str): User's email
        code (str): Reset code
        new_password (str): New password
        db (AsyncSession): Database session

    Returns:
        dict: Password reset status
    """
    return await reset_password(db, email, code, new_password)


@router.post("/logout", response_model=dict)
async def logout(current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    """
    Logout current user.

    Args:
        current_user (User): Authenticated user
        db (AsyncSession): Database session

    Returns:
        dict: Logout status
    """
    return await logout_user(db, current_user)
