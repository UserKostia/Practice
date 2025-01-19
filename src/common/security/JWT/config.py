from pathlib import Path

from dotenv import dotenv_values
from pydantic import BaseModel

# Path value for base project directory
BASE_DIR = Path(__file__).resolve().parent

# Download values from .env file
config_credentials = dotenv_values(".env")


# Class for containing pathes to private and public keys
class AuthJWT(BaseModel):
    private_key_path: Path = BASE_DIR / "src" / "common" / "JWT" / "certs" / "jwt-public.pem"
    public_key_path: str = config_credentials["SECRET_JWT_KEY"]
    algorithm: str = "RS256"
    access_token_expire_minutes: int = 1000


authjwt = AuthJWT()

PRIVATE_KEY = authjwt.private_key_path
PUBLIC_KEY = authjwt.public_key_path
ALGORITHM = authjwt.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = authjwt.access_token_expire_minutes
