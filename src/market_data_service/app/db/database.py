from src.common.db.database import create_engine_and_session
from src.common.db.config import MARKET_DATA_DATABASE_URL

# Connecton to market_data_service DB
engine, AsyncSessionLocal = create_engine_and_session(MARKET_DATA_DATABASE_URL)
