from pydantic import BaseModel, Field, field_validator

from typing import Optional
from datetime import date, datetime

from src.auth_service.app.validators.password import PasswordValidator
from src.auth_service.app.validators.birthdate import BirthdateValidator
from src.auth_service.app.validators.username import UsernameValidator


class UserProfileBase(BaseModel):
    """
    Base schema for user.

    :param
     username: User`s username
     birthdate: User`s birthdate
     ava_url: User`s avatar
     bio: User`s biography
    """

    username: Optional[str] = Field(..., min_length=3, max_length=40)
    birthdate: Optional[date] = None
    ava_url: Optional[str] = None
    bio: Optional[str] = None

    @field_validator("username")
    def validate_username(cls, value: str) -> str:
        return UsernameValidator().validate(value)

    @field_validator("birthdate")
    def validate_birthdate(cls, value: date) -> date:
        return BirthdateValidator().validate(value)


class UserProfileCreate(UserProfileBase):
    """
    Shema for user creation (registration).

    :param
    password: User`s password
    """
    password: str = Field(..., min_length=8, max_length=32)

    @field_validator("password")
    def validate_password(cls, value: str) -> str:
        return PasswordValidator().validate(value)


class UserProfileUpdate(UserProfileBase):
    """
    Shema for user update full.
    """
    birthdate: Optional[date] = Field(...)
    ava_url: Optional[str] = Field(...)
    bio: Optional[str] = Field(...)


class UserProfileUpdatePartial(BaseModel):
    """
    Shema for user update partial.
    """
    username: Optional[str] = Field(None, min_length=3, max_length=40)
    birthdate: Optional[date] = None
    ava_url: Optional[str] = None
    bio: Optional[str] = None


class UserProfileResponse(UserProfileBase):
    """
    Shema for user response.

    :param
    id: User`s id
    created_at: User`s creation date and time
    updated_at: User`s last update date and time

    """
    id: int = Field(...)
    created_at: datetime = Field(...)
    updated_at: datetime = Field(...)

    class Config:
        orm_mode = True  # Allows to work with SQLAlchemy-models

    # model_config = ConfigDict(
    #     from_attributes=True
    # )
