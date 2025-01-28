import string
import random
from datetime import datetime, timedelta

from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status

from src.identity_service.app.models.user import User
from src.identity_service.app.repositories.user import get_user_by_email, authenticate_user as authenticate_user_repo
from src.identity_service.app.schemas.user import UserLogin
from src.identity_service.app.utils.password import verify_password
from src.common.security.JWT.utils import encode_jwt
from src.common.security.JWT.config import ACCESS_TOKEN_EXPIRE_MINUTES


async def authenticate_user(db: AsyncSession, user_login: UserLogin) -> User:
    """
    Authenticate user using login credentials

    Args:
        db (AsyncSession): Database session
        user_login (UserLogin): User login credentials

    Returns:
        User: Authenticated user

    Raises:
        HTTPException: If authentication fails
    """
    user = await get_user_by_email(db, user_login.email)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    if not verify_password(user_login.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid password")

    if not user.is_verified:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Please confirm your email")

    return user


def create_access_token(data: dict, expires_delta: timedelta = None) -> str:
    """
    Generate access JWT token

    Args:
        data (dict): Token payload
        expires_delta (timedelta, optional): Token expiration time

    Returns:
        str: JWT access token
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})
    return encode_jwt(payload=to_encode)


def create_refresh_token(data: dict) -> str:
    """
    Generate refresh JWT token

    Args:
        data (dict): Token payload

    Returns:
        str: JWT refresh token
    """
    return create_access_token(
        data,
        expires_delta=timedelta(days=7)
    )


def generate_confirmation_code(length: int = 6) -> str:
    """
    Generate random confirmation code

    Args:
        length (int, optional): Code length. Defaults to 6.

    Returns:
        str: Confirmation code
    """
    return ''.join(random.choices(string.digits, k=length))


def generate_reset_code(length: int = 6) -> str:
    """
    Generate random reset code for password reset

    Args:
        length (int, optional): Code length. Defaults to 6.

    Returns:
        str: Reset code
    """
    return generate_confirmation_code(length)
