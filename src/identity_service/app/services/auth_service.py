from fastapi import HTTPException, status
from pydantic import EmailStr
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.identity_service.app.repositories.user import get_user
from src.identity_service.app.models.user import User
from src.identity_service.app.schemas.token import Token
from src.identity_service.app.utils.email import send_verification_email, send_password_reset_email
from src.identity_service.app.utils.password import get_password_hash
from src.identity_service.app.utils.security import create_access_token, create_refresh_token, generate_confirmation_code, \
    generate_reset_code
from src.common.security.JWT.utils import decode_jwt


async def refresh_access_token(db: AsyncSession, refresh_token: str) -> Token:
    """
    Update Access Token using Refresh Token.
    """
    try:
        # Decode refresh token
        payload = decode_jwt(refresh_token)

        # Get user`s ID
        user_id = payload.get("id")

        # If user`s ID not exists generate exception
        if not user_id:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")

        # If user not exists generate exception
        user = await get_user(db, user_id)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

        # Generate new Access and Refresh Tokens
        access_token = create_access_token({"id": user.id, "email": user.email})
        refresh_token = create_refresh_token({"id": user.id, "email": user.email})

        token = Token(access_token=access_token, refresh_token=refresh_token)

        return token

    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")


async def register_user(db: AsyncSession, email: EmailStr, password: str) -> dict:
    """
    User Registration with Email confirmation.
    """
    # Check user exists
    user = await db.execute(select(User).filter(User.email == email))
    user = user.scalars().first()

    if user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Користувач вже існує")

    # Generate confirmation code
    confirmation_code = generate_confirmation_code()

    # Password hashing
    hashed_password = get_password_hash(password)

    # Creating new user
    new_user = User(email=email, hashed_password=hashed_password, confirmation_code=confirmation_code)
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    # Send verification letter
    await send_verification_email(email, confirmation_code)

    return {"message": "Verification email sent."}


async def verify_email(db: AsyncSession, email: str, code: str) -> dict:
    """
    Confirm email by code.
    """

    # Select user by email
    user = await db.execute(select(User).filter(User.email == email))
    user = user.scalars().first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    if user.is_verified:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already verified")

    if user.confirmation_code != code:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid confirmation code")

    # Account confirmation
    user.is_verified = True
    user.confirmation_code = None
    await db.commit()

    return {"message": "Email successfully verified"}


async def request_password_reset(db: AsyncSession, email: EmailStr) -> dict:
    """
    Generate password reset code for email.
    """
    user = await db.execute(select(User).filter(User.email == email))
    user = user.scalars().first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Користувача не знайдено")

    # Генерація коду
    reset_code = generate_reset_code()
    user.reset_password_code = reset_code
    await db.commit()

    # Надсилання коду
    await send_password_reset_email(email, reset_code)

    return {"message": "Password reset email sent."}


async def reset_password(db: AsyncSession, email: str, code: str, new_password: str) -> dict:
    """
    Update user`s password after confirmation code.
    """
    user = await db.execute(select(User).filter(User.email == email))
    user = user.scalars().first()

    if not user or user.reset_password_code != code:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Невірний код відновлення")

    # Password update
    user.hashed_password = get_password_hash(new_password)
    user.reset_password_code = None
    await db.commit()

    return {"message": "Password successfully updated."}


async def logout_user(db: AsyncSession, user: User) -> dict:
    """
    Logout user.
    """
    # Clear Refresh Token
    user.refresh_token = None
    await db.commit()

    return {"message": "You have been logged out."}
