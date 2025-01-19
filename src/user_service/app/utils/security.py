from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from src.user_service.app.models.user_profile import UserProfile


async def is_user_profile_exists(db: AsyncSession, user_profile) -> bool:
    """
    :param user_profile:
    :param db:
    :return: bool
    """

    profile = await db.execute(select(UserProfile).where(UserProfile.id == user_profile.id))

    if profile.scalars().first():
        return True

    return False
