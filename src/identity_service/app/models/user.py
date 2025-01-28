from pydantic import EmailStr
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Date, func
from src.common.db.base import Base


class User(Base):
    """
    SQLAlchemy ORM model for table 'users'.

    Represents system users and stores information about their login credentials,
    personal details, and metadata.

    Attributes:
        id (int): The unique identifier for the user.
        email (EmailStr): The user's email address.
        hashed_password (str): The hashed password for the user.
        is_verified (bool): Indicates if the user's email is verified.
        confirmation_code (str): The code for email verification.
        reset_password_code (str): The code for resetting the password.
        username (str): The user's unique username.
        birthdate (Optional[date]): The user's birthdate.
        ava_url (Optional[str]): The URL of the user's avatar image.
        bio (Optional[str]): A short biography for the user.
        created_at (datetime): The timestamp when the user was created.
        updated_at (datetime): The timestamp when the user was last updated.
    """
    __tablename__ = "users"

    # Authentication fields
    id = Column(Integer, primary_key=True, index=True)
    email = Column(EmailStr, unique=True, nullable=False, index=True)
    hashed_password = Column(String, nullable=False)
    is_verified = Column(Boolean, default=False)
    confirmation_code = Column(String(6), default=None)
    reset_password_code = Column(String(6), default=None)

    # Profile fields
    username = Column(String(40), unique=True, nullable=False)
    birthdate = Column(Date, nullable=True)
    ava_url = Column(String, default="assets/default_avatar.png")
    bio = Column(String, nullable=True)

    # Metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
