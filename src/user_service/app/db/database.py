from src.common.db.database import create_engine_and_session
from src.common.db.config import USER_DATABASE_URL

# Connecton to user_service DB
engine, AsyncSessionLocal = create_engine_and_session(USER_DATABASE_URL)
