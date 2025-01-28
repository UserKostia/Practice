from src.common.db.database import create_engine_and_session
from src.common.db.config import IDENTITY_DATABASE_URL

# Connecton to identity_service DB
engine, AsyncSessionLocal = create_engine_and_session(IDENTITY_DATABASE_URL)
