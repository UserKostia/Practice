from sqlalchemy import Column, Integer, String, Date, DateTime, func

from src.common.db.base import Base


class UserProfile(Base):
    __tablename__ = "user_profiles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, unique=True, nullable=False)  # 🔑 Посилання на користувача з auth_service
    username = Column(String, unique=True, nullable=False)
    birthdate = Column(Date, nullable=True)
    ava_url = Column(String, default="assets/default_avatar.png")
    bio = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
