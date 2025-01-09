from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Optional
from datetime import date

from src.auth_service.app.validators.password import PasswordValidator


class UserBase(BaseModel):
    """
    Base schema for user.

    :param
     email: User`s email
     username: User`s username
     birthdate: User`s birthdate

     ...: indicates that current field is required and None if not
    """
    email: EmailStr = Field(...)
    username: Optional[str] = Field(..., max_length=50)
    birthdate: Optional[date] = Field(None)


class UserCreate(UserBase):
    """
    Shema for user creation (registration).

    :param
    password: User`s password

    :description:
    password: User`s password must be at least 8 characters long and no more than 128 characters long.
    """
    password: str = Field(..., min_length=8, max_length=128)

    @field_validator("password")
    def validate_password(cls, value: str) -> str:
        password_validator = PasswordValidator()
        return password_validator.validate(value)


class UserResponse(UserBase):
    """
    Shema for user response.

    :param
    id: User`s id
    is_verified: indicator if user is verified after email verification
    ava_url: User`s avatar url

    """
    id: int = Field(..., description="Унікальний ідентифікатор користувача")
    is_verified: bool = Field(default=False, description="Чи підтверджений користувач")
    ava_url: str = Field(default="assets/default_avatar.png", description="URL аватара користувача")

    class Config:
        orm_mode = True  # Allows to work with SQLAlchemy-models
