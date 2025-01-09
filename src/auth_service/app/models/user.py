from sqlalchemy import Column, Integer, String, Date, Boolean, DateTime, func
from src.auth_service.app.db.database import Base


class User(Base):
    """
    SQLAlchemy ORM model for table 'users'.

    Introduces system users, stores information about
    their emails, passwords, verification status, and other details.

    Table name:
        users
    """

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    """
    Unique user identifier.

    :type: Integer
    """

    email = Column(String, unique=True, nullable=False, index=True)
    """
    The user's email. Must be unique and mandatory.

    :type: String
    """

    username = Column(String, nullable=False)
    """
    The user's username. Must be mandatory.

    :type: String
    """

    hashed_password = Column(String, nullable=False)
    """
    The user's hashed password. Must be mandatory and not empty.

    :type: String
    """

    birthdate = Column(Date, nullable=True)
    """
    The user's birthdate. Must be mandatory and not empty if the user is 18+.

    :type: Date
    """

    ava_url = Column(String, default="assets/default_avatar.png")
    """
    URL to the user's avatar. By default, it points to the standard avatar.

    :type: String
    """

    token = Column(String, default="")
    """
    Token for sessions or password recovery.

    :type: String
    """

    is_verified = Column(Boolean, default=False)
    """
    User verification status.

    :type: Boolean
    """

    confirmation_code = Column(String(6), default=None)
    """
    Verification code to verify or recover your password.

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
