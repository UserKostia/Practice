import string
import random
import datetime
from datetime import datetime, timedelta

from pydantic import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from src.auth_service.app.models.user import AuthUser
from src.auth_service.app.crud.user import get_user_by_email
from src.auth_service.app.utils.password import verify_password
from src.common.security.JWT.utils import encode_jwt
from src.common.security.JWT.config import ACCESS_TOKEN_EXPIRE_MINUTES


async def authenticate_user(db: AsyncSession, email: EmailStr, password: str) -> AuthUser:
    """
    Authenticate user using email and password
    """
    user = await get_user_by_email(db, email)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Користувач не знайдено")

    if not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Невірний пароль")

    if not user.is_verified:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Підтвердіть email")

    return user


def create_access_token(data: dict) -> str:
    """
    Generate access JWT token
    """
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    data.update({"exp": expire})
    token = encode_jwt(payload=data)
    return token


def create_refresh_token(data: dict) -> str:
    """
    Generate refresh JWT token
    """
    expire = datetime.utcnow() + timedelta(days=7)
    data.update({"exp": expire})
    token = encode_jwt(payload=data)
    return token


def generate_confirmation_code(length: int = 6) -> str:
    """
    Generate random confirmation code
    """
    return ''.join(random.choices(string.digits, k=length))


def generate_reset_code(length: int = 6) -> str:
    """
    Generate random reset code for reset password.
    """
    return ''.join(random.choices(string.digits, k=length))
