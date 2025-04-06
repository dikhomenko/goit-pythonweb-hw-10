from pathlib import Path
from pydantic_settings import BaseSettings
from pydantic import EmailStr
from typing import ClassVar


class Settings(BaseSettings):

    # Local DB configuration
    DATABASE_URL: str

    # Token configuration for JWT authentication
    SECRET_KEY: str
    ALGORITHM: str
    JWT_EXPIRATION_SECONDS: int

    # Origins for CORS policy
    ORIGINS: list[str] = ["http://localhost:3000", "http://127.0.0.1:8000"]

    OAUTH2_SCHEME: str = "/api/auth/login"

    # Email configuration for sending emails
    MAIL_USERNAME: EmailStr
    MAIL_PASSWORD: str
    MAIL_FROM: EmailStr
    MAIL_PORT: int
    MAIL_SERVER: str
    MAIL_FROM_NAME: str = "Dina Rest API Service"
    MAIL_STARTTLS: bool = False
    MAIL_SSL_TLS: bool = True
    USE_CREDENTIALS: bool = True
    VALIDATE_CERTS: bool = True

    # Cloudinary configuration to store images
    CLOUDINARY_NAME: str
    CLOUDINARY_API_KEY: int
    CLOUDINARY_API_SECRET: str

    # PostgreSQL configuration for Docker
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str

    class Config:
        env_file = str(Path(__file__).parent.parent / ".env")


settings = Settings()
