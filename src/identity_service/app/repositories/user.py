from typing import List
from fastapi import HTTPException
from pydantic import EmailStr
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.identity_service.app.models.user import User
from src.identity_service.app.schemas.user import UserCreate, UserLogin, UserUpdate
from src.identity_service.app.utils.password import get_password_hash, verify_password


async def create_user(db: AsyncSession, user_in: UserCreate) -> User:
    """
    Creates a new user in the database.

    Args:
        db (AsyncSession): The database session.
        user_in (UserCreate): User creation data transfer object.

    Returns:
        User: The newly created user object.

    Raises:
        HTTPException: If a user with the same email or username already exists.
    """
    # Check for existing user with same email or username
    existing_user = await db.execute(
        select(User).where(
            (User.email == user_in.email) | (User.username == user_in.username)
        )
    )
    if existing_user.scalars().first():
        raise HTTPException(status_code=400, detail="User with this email or username already exists")

    # Hash the password before storing
    hashed_password = get_password_hash(user_in.password)

    # Create new user instance
    new_user = User(
        email=user_in.email,
        username=user_in.username,
        hashed_password=hashed_password,
        birthdate=user_in.birthdate,
        ava_url=user_in.ava_url,
        bio=user_in.bio
    )

    # Persist user to database
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    return new_user


async def authenticate_user(db: AsyncSession, user_login: UserLogin) -> User:
    """
    Authenticates a user by email and password.

    Args:
        db (AsyncSession): The database session.
        user_login (UserLogin): User login credentials.

    Returns:
        User: The authenticated user object.

    Raises:
        HTTPException: If authentication fails due to incorrect credentials.
    """
    # Retrieve user by email
    user = await db.execute(select(User).where(User.email == user_login.email))
    user = user.scalars().first()

    # Verify credentials
    if not user or not verify_password(user_login.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Incorrect email or password")

    return user


async def get_user(db: AsyncSession, user_id: int) -> User:
    """
    Retrieves a user by their unique identifier.

    Args:
        db (AsyncSession): The database session.
        user_id (int): The unique identifier of the user.

    Returns:
        User: The user object corresponding to the given ID.

    Raises:
        HTTPException: If no user is found with the specified ID.
    """
    user = await db.execute(select(User).where(User.id == user_id))
    user = user.scalars().first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user


async def get_user_by_email(db: AsyncSession, email: EmailStr) -> User:
    """
    Retrieves a user by their email address.

    Args:
        db (AsyncSession): The database session.
        email (str): The email address of the user.

    Returns:
        User: The user object corresponding to the given email.

    Raises:
        HTTPException: If no user is found with the specified email.
    """
    user = await db.execute(select(User).where(User.email == email))
    user = user.scalars().first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user


async def get_users(db: AsyncSession, skip: int = 0, limit: int = 100) -> List[User]:
    """
    Retrieves a list of users with optional pagination.

    Args:
        db (AsyncSession): The database session.
        skip (int, optional): Number of users to skip for pagination. Defaults to 0.
        limit (int, optional): Maximum number of users to return. Defaults to 100.

    Returns:
        List[User]: A list of user objects.
    """
    users = await db.execute(select(User).offset(skip).limit(limit))
    return list(users.scalars().all())


async def update_user(
        db: AsyncSession,
        user_id: int,
        user_update: UserUpdate
) -> User:
    """
    Updates an existing user's profile.

    Args:
        db (AsyncSession): The database session.
        user_id (int): The unique identifier of the user to update.
        user_update (UserUpdate): The user update data transfer object.

    Returns:
        User: The updated user object.

    Raises:
        HTTPException: If the user is not found.
    """
    # Retrieve existing user
    user = await get_user(db, user_id)

    # Process update data
    update_data = user_update.model_dump(exclude_unset=True)

    # Handle password update separately
    if update_data.get('password'):
        update_data['hashed_password'] = get_password_hash(update_data.pop('password'))

    # Apply updates
    for key, value in update_data.items():
        setattr(user, key, value)

    # Persist changes
    await db.commit()
    await db.refresh(user)

    return user


async def delete_user(db: AsyncSession, user_id: int) -> None:
    """
    Deletes a user from the database.

    Args:
        db (AsyncSession): The database session.
        user_id (int): The unique identifier of the user to delete.

    Raises:
        HTTPException: If the user is not found.
    """
    # Retrieve and validate user existence
    user = await get_user(db, user_id)

    # Remove user from database
    await db.delete(user)
    await db.commit()
