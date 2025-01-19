from src.common.db.database import create_engine_and_session
from src.common.db.config import AUTH_DATABASE_URL

# Connection to auth_service DB
engine, AsyncSessionLocal = create_engine_and_session(AUTH_DATABASE_URL)
