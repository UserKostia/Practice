import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# Connection to db for identity_service
IDENTITY_DATABASE_URL = os.getenv("IDENTITY_DATABASE_URL", "sqlite+aiosqlite:///./identity.db")

# Connection to db for market_data_service
MARKET_DATA_DATABASE_URL = os.getenv("MARKET_DATA_DATABASE_URL", "sqlite+aiosqlite:///./market_data.db")
