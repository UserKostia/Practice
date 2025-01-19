from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth_service.app.services.auth_service import refresh_access_token, verify_email, request_password_reset, \
    reset_password, logout_user
from src.common.db.database import get_db
from src.common.user_data import get_current_user

from src.auth_service.app.crud.user import create_user, get_user_by_email
from src.auth_service.app.models.user import AuthUser
from src.auth_service.app.schemas.token import Token
from src.auth_service.app.schemas.user import AuthUserCreate, AuthUserLogin, AuthUserResponse
from src.auth_service.app.utils.security import create_access_token, authenticate_user

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/sign-up", response_model=Token, status_code=status.HTTP_201_CREATED)
async def sign_up(user_in: AuthUserCreate, db: AsyncSession = Depends(get_db)):
    """
    Register new user.
    """

    # Is user exists
    existing_user = await get_user_by_email(db, user_in.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Користувач із таким email вже існує")

    # Create user
    new_user = await create_user(db, user_in)

    # Generate token
    access_token = create_access_token(data={"id": new_user.id, "email": new_user.email})

    # Create token
    token = Token(access_token=access_token, token_type="bearer")

    return token


@router.post("/sign-in", response_model=Token)
async def sign_in(user_in: AuthUserLogin, db: AsyncSession = Depends(get_db)):
    """
    User entrance. Checked email and password.
    """

    # Authenticate user
    user = await authenticate_user(db, user_in.email, user_in.password)

    # Generate JWT access token
    access_jwt_token = create_access_token(data={"id": user.id, "email": user.email})

    # Generate JWT refresh token
    refresh_jwt_token = create_access_token(data={"id": user.id, "email": user.email})

    # Create token
    token = Token(access_token=access_jwt_token, refresh_token=refresh_jwt_token)

    return token


@router.get("/me", response_model=AuthUserResponse)
async def read_current_user(current_user: AuthUser = Depends(get_current_user)):
    """
    Return current user.
    """
    user = {"email": current_user.email, "id": current_user.id}

    return user


@router.post("/refresh-token", response_model=Token)
async def refresh_token(refresh_token: str, db: AsyncSession = Depends(get_db)):
    """
    Update Access Token using Refresh Token.
    """
    token = await refresh_access_token(db, refresh_token)
    return token


@router.post("/verify-email", response_model=dict)
async def verify_email_route(email: str, code: str, db: AsyncSession = Depends(get_db)):
    """
    Confirmation email.
    """
    await verify_email(db, email, code)
    return {"message": "Email confirmed."}


@router.post("/forgot-password", response_model=dict)
async def forgot_password(email: EmailStr, db: AsyncSession = Depends(get_db)):
    """
    Reques for reset password (generating and sending code).
    """
    request = await request_password_reset(db, email)
    return request


@router.post("/reset-password", response_model=dict)
async def reset_password_route(email: str, code: str, new_password: str, db: AsyncSession = Depends(get_db)):
    """
    Recover password after code confirmation.
    """
    reset = await reset_password(db, email, code, new_password)
    return reset


@router.post("/logout", response_model=dict)
async def logout(current_user: AuthUser = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    """
    Logout current user from system.
    """
    user_logout = await logout_user(db, current_user)
    return user_logout
