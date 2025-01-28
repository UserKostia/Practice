from typing import Optional
from pydantic import BaseModel, EmailStr, Field, field_validator
from datetime import date, datetime

from src.identity_service.app.validators.password import PasswordValidator


class UserBase(BaseModel):
    """
    Base schema for a user.

    Attributes:
        email (EmailStr): The user's email.
        username (str): The user's username.
        birthdate (Optional[date]): The user's birthdate.
        ava_url (Optional[str]): The user's avatar URL.
        bio (Optional[str]): The user's bio.
    """
    email: EmailStr
    username: str
    birthdate: Optional[date] = None
    ava_url: Optional[str] = "assets/default_avatar.png"
    bio: Optional[str] = None

    class Config:
        orm_mode = True


class UserCreate(UserBase):
    """
    Schema for creating a new user.

    Attributes:
        password (str): The user's password.
    """
    password: str = Field(..., min_length=8, max_length=32)

    @field_validator("password")
    def validate_password(cls, value: str) -> str:
        """Validates the user's password."""
        return PasswordValidator().validate(value)


class UserResponse(UserBase):
    """
    Schema for returning user information.

    Attributes:
        id (int): The unique identifier for the user.
        is_verified (bool): Indicates if the user is verified.
        created_at (datetime): The timestamp when the user was created.
        updated_at (datetime): The timestamp when the user was last updated.
    """
    id: int
    is_verified: bool
    created_at: datetime
    updated_at: datetime


class UserUpdate(UserBase):
    """
    Schema for updating user information.

    Attributes:
        password (Optional[str]): The new password for the user.
        is_verified (Optional[bool]): Indicates if the user is verified.
        confirmation_code (Optional[str]): A code for verifying the account or resetting the password.
    """
    password: Optional[str] = Field(None, min_length=8, max_length=32)
    is_verified: Optional[bool] = None
    confirmation_code: Optional[str] = Field(None, min_length=6, max_length=6)

    @field_validator("password")
    def validate_password(cls, value: str) -> str:
        """Validates the user's password."""
        return PasswordValidator().validate(value)


class UserLogin(BaseModel):
    """
    Schema for user login.

    Attributes:
        email (EmailStr): The user's email for login.
        password (str): The user's password for login.
    """
    email: EmailStr = Field(...)
    password: str = Field(..., min_length=8, max_length=32)
