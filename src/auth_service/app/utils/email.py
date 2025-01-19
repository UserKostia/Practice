import configparser

from pydantic import EmailStr
from dotenv import dotenv_values
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig


# Download values from .env file
config_credentials = dotenv_values(".env")

# Download configuration from config.ini
config = configparser.ConfigParser()
config.read('config.ini')

# Check API key exists
if 'DEFAULT' not in config or 'API_KEY' not in config['DEFAULT']:
    raise ValueError("API_KEY not found in config.ini")

api_key = config['DEFAULT']['API_KEY']

# Email settings
conf = ConnectionConfig(
    MAIL_USERNAME=config_credentials["EMAIL"],
    MAIL_PASSWORD=api_key,
    # MAIL_PASSWORD=config_credentials["PASS"],
    MAIL_FROM=config_credentials["EMAIL"],
    MAIL_FROM_NAME="Cryptotracker",
    MAIL_PORT=587,
    MAIL_SERVER="smtp.sendgrid.net",
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True,
)


async def send_verification_email(email: EmailStr, confirmation_code: str):
    """
    Sends a verification email for verify user email.
    """
    message = MessageSchema(
        subject="Email Confirmation",
        recipients=[email],
        body=f"Your confirmation code: {confirmation_code}",
        subtype="plain"
    )

    fm = FastMail(conf)
    await fm.send_message(message)


async def send_password_reset_email(email: EmailStr, reset_code: str):
    """
    Send a password reset email.
    """
    message = MessageSchema(
        subject="Password Reset",
        recipients=[email],
        body=f"Your code to reset password: {reset_code}",
        subtype="plain"
    )

    fm = FastMail(conf)
    await fm.send_message(message)
