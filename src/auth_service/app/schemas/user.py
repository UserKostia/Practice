from typing import Optional
from datetime import datetime

from pydantic import BaseModel, EmailStr, Field, field_validator

from src.auth_service.app.validators.password import PasswordValidator


class AuthUserBase(BaseModel):
    """
    Base schema for user authentication.

     :param email: User`s email

    """
    email: EmailStr = Field(...)


class AuthUserCreate(AuthUserBase):
    """
    Shema for user creation (registration).

    :param password: User`s password
    """
    password: str = Field(..., min_length=8, max_length=32)

    @field_validator("password")
    def validate_password(cls, value: str) -> str:
        return PasswordValidator().validate(value)


class AuthUserResponse(AuthUserBase):
    """
    Shema for user response.

    :param
    id: User`s id
    is_verified: indicator if user is verified after email verification
    created_at: User`s creation date and time
    updated_at: User`s last update date and time

    """
    id: int = Field(...)
    is_verified: bool = Field(default=False)
    created_at: datetime = Field(...)
    updated_at: datetime = Field(...)

    class Config:
        orm_mode = True  # Allows to work with SQLAlchemy-models

    # model_config = ConfigDict(
    #     from_attributes=True
    # )


class AuthUserUpdate(AuthUserBase):
    """
    Shema for update password or account confirmation.

    :param password: New password.
    :param is_verified: Update confirmation status.
    :param confirmation_code: Confirmation code.
    """

    password: Optional[str] = Field(None, min_length=8, max_length=32)
    is_verified: Optional[bool] = Field(None)
    confirmation_code: Optional[str] = Field(None, min_length=6, max_length=6)

    @field_validator("password")
    def validate_password(cls, value: str) -> str:
        return PasswordValidator().validate(value)


class AuthUserLogin(BaseModel):
    """
    Схема для входу користувача.
    """
    email: EmailStr = Field(...)
    password: str = Field(..., min_length=8, max_length=32)
