from pydantic import EmailStr
from sqlalchemy import Column, Integer, String, Boolean, DateTime, func

from src.common.db.base import Base


class AuthUser(Base):
    """
    SQLAlchemy ORM model for table 'users'.

    Introduces system users, stores information about
    their emails, passwords, verification status, and other details.

    Table name:
        auth_users
    """

    __tablename__ = "auth_users"

    id = Column(Integer, primary_key=True, index=True)
    """
    Unique user identifier.

    :type: Integer
    """

    email = Column(EmailStr, unique=True, nullable=False, index=True)
    """
    The user's email. Must be unique and mandatory.

    :type: String
    """

    hashed_password = Column(String, nullable=False)
    """
    The user's hashed password. Must be mandatory and not empty.

    :type: String
    """

    is_verified = Column(Boolean, default=False)
    """
    User verification status.

    :type: Boolean
    """

    confirmation_code = Column(String(6), default=None)
    """
    Verification code to verify your password.

    :type: String(6)
    """

    reset_password_code = Column(String(6), default=None)
    """
    Password recovery code.

    :type: String(6)
    """

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    """
    The time when the record was created. Filled in automatically.

    :type: DateTime
    """

    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    """
    Time when the record was last updated. It is updated automatically.

    :type: DateTime
    """
