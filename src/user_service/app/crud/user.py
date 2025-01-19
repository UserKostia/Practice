from typing import Union

from fastapi import HTTPException

from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.user_service.app.models.user_profile import UserProfile
from src.user_service.app.schemas.user import UserProfileUpdate, UserProfileCreate, UserProfileUpdatePartial
from src.user_service.app.utils.security import is_user_profile_exists


async def create_user_profile(db: AsyncSession, user_profile_in: UserProfileCreate) -> UserProfile:
    """
    Create a new user profile

    :param db:
    :param user_profile_in:
    :return user_profile:
    """

    # Check if the user profile already exists
    if await is_user_profile_exists(db, user_profile_in):
        raise HTTPException(status_code=400, detail="User already exists.")

    # Create a dictionary from the inputed data
    user_profile_data: dict = user_profile_in.model_dump()

    # Create a new user profile object
    user_profile = UserProfile(**user_profile_data)

    # Add a new user profile object to database
    db.add(user_profile)

    # Commit changes
    await db.commit()

    return user_profile


async def get_user_profile(db: AsyncSession, user_profile_id: int) -> UserProfile:
    """

    :param db:
    :param user_profile_id:
    :return:
    """

    # Select one user profile by id
    user_profile = await db.execute(select(UserProfile).where(UserProfile.id == user_profile_id))
    user_profile = user_profile.scalars().first()

    # Check if the user profile is exist
    if not user_profile:
        raise HTTPException(status_code=404, detail="User profile not found.")

    return user_profile


async def get_user_profiles(db: AsyncSession) -> list[UserProfile]:
    """
    Get all user profiles.

    :param db:
    :return:
    """

    # Get all user profiles
    user_profiles = await db.execute(select(UserProfile))
    user_profiles = user_profiles.scalars().all()

    # Convert to list
    user_profiles = list(user_profiles)

    return user_profiles


async def update_user_profile(
        db: AsyncSession, user_profile_id: int,
        user_update: Union[UserProfileUpdate, UserProfileUpdatePartial], exclude_none: bool = False
) -> UserProfile:
    """
    Update user profile data.

    :param db:
    :param user_profile_id:
    :param user_update:
    :param exclude_none:
    :return user:
    """

    # Get user profile
    user_profile = await get_user_profile(db, user_profile_id)

    # Check user profile exists
    if not user_profile:
        raise HTTPException(status_code=404, detail="User profile not found.")

    # Select updatated filds
    user_profile_update_data = user_update.model_dump(exclude_none=exclude_none)

    # Update user profile attributes
    for key, value in user_profile_update_data.items():
        setattr(user_profile, key, value)

    # Commit changes
    await db.commit()

    # Refresh object in db
    await db.refresh(user_profile)

    return user_profile


async def delete_user_profile(db: AsyncSession, user_profile_id: int) -> None:
    """
    Delete user profile.

    :param db:
    :param user_profile_id:
    :return:
    """

    # Get user_profile by id
    user_profile = await get_user_profile(db, user_profile_id)

    # Delete user profile
    await db.delete(user_profile)

    # Commit changes
    await db.commit()

    return None
