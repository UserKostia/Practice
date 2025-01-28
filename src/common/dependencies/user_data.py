from jose import JWTError, jwt

from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, status, HTTPException

from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.identity_service.app.repositories.user import get_user
from src.identity_service.app.models.user import User

from src.common.db.database import get_db
from src.common.security.JWT.config import PRIVATE_KEY, ALGORITHM, PUBLIC_KEY


oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/token")

# JWT constants
JWT_PRIVATE_KEY: str = PRIVATE_KEY.read_text()
JWT_PUBLIC_KEY: str = PUBLIC_KEY.read_text()


async def get_current_user(
    token: str = Depends(oauth2_bearer), db: AsyncSession = Depends(get_db)
) -> User:
    """
    Get the current authenticated user based on JWT token.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        # Decode data from token and get user id from dict
        payload = jwt.decode(token, JWT_PRIVATE_KEY, algorithms=[ALGORITHM])
        user_id: int = payload.get("id")

    except JWTError:
        raise credentials_exception

    # Get user by id if exists
    user = await get_user(db=db, user_id=int(user_id))
    if user is None:
        raise credentials_exception

    return user
