from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.common.utils.logginig_config import setup_logging
from src.identity_service.app.routers.user import router as identity_router

setup_logging()

app = FastAPI(
    title="Identity service",
    description="This is a microservice for user sign-in, sign-up, and authentication and user management.",
    version="1.0.0",
    contact={
        "name": "Kostiantyn Striletskyi",
        "email": "kostastriletski@gmail.com",
    },
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace "*" with specific origins for better security
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

# Include routers
app.include_router(router=identity_router)
