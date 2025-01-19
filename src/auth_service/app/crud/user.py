import logging

from typing import List

from fastapi import HTTPException
from pydantic import EmailStr
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth_service.app.models.user import AuthUser
from src.auth_service.app.schemas.user import AuthUserCreate
from src.auth_service.app.utils.password import get_password_hash

# Logger settings
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def create_user(db: AsyncSession, user_in: AuthUserCreate) -> AuthUser:
    """
    📌 Створення нового користувача.
    """

    hashed_password = get_password_hash(user_in.password)

    new_user = AuthUser(
        email=user_in.email,
        hashed_password=hashed_password,
    )

    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    return new_user


# async def create_user(db: AsyncSession, user_in: AuthUserCreate) -> AuthUser:
#     """Create a new user."""
#
#     # Check if the user already exists
#     if await check_user_exists(db, user_in):
#         raise HTTPException(status_code=400, detail="User already exists.")
#
#     # Prepare user data
#     user_data = user_in.model_dump()
#
#     # Visualize user password in terminal with logger
#     logger.info(f"PASSWORD : {user_data['password']}")
#
#     user_data["hashed_password"] = get_password_hash(user_in.password)
#
#     # Create new user instance
#     new_user = AuthUser(**user_data)
#
#     db.add(new_user)
#     await db.commit()
#     await db.refresh(new_user)
#
#     return new_user


async def get_user(db: AsyncSession, user_id: int) -> AuthUser:
    """Get user by id."""
    user = await db.execute(select(AuthUser).where(AuthUser.id == user_id))
    user = user.scalars().first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found.")

    return user


async def get_user_by_email(db: AsyncSession, email: EmailStr) -> AuthUser:
    """Get user by email."""

    user = await db.execute(select(AuthUser).where(AuthUser.email == email))
    user = user.scalars().first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found.")

    return user


async def get_users(db: AsyncSession) -> List[AuthUser]:
    """Get a list of all users."""
    users = await db.execute(select(AuthUser))
    return list(users.scalars().all())
