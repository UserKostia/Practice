import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# Connection to db for auth_service
AUTH_DATABASE_URL = os.getenv("AUTH_DATABASE_URL", "sqlite+aiosqlite:///./auth.db")

# Connection to db for user_service
USER_DATABASE_URL = os.getenv("USER_DATABASE_URL", "sqlite+aiosqlite:///./user.db")
