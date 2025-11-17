from pydantic_settings import BaseSettings
from pydantic import Field, field_validator
from typing import Optional
import os

class Settings(BaseSettings):
    # Database
    database_url: str = Field(
        default="postgresql://user:password@localhost/omnilead",
        description="PostgreSQL database connection URL"
    )

    # Redis
    redis_url: str = Field(
        default="redis://localhost:6379",
        description="Redis connection URL"
    )

    # OpenAI
    openai_api_key: Optional[str] = Field(
        default=None,
        description="OpenAI API key for AI services"
    )
    openai_model: str = Field(
        default="gpt-4",
        description="OpenAI model to use"
    )

    # JWT
    secret_key: str = Field(
        default="your-secret-key-change-in-production",
        description="Secret key for JWT token signing. MUST be changed in production!"
    )
    algorithm: str = Field(
        default="HS256",
        description="JWT algorithm"
    )
    access_token_expire_minutes: int = Field(
        default=30,
        description="JWT access token expiration time in minutes"
    )

    # Webhook secrets
    whatsapp_webhook_secret: Optional[str] = Field(
        default=None,
        description="WhatsApp webhook verification secret"
    )
    facebook_webhook_secret: Optional[str] = Field(
        default=None,
        description="Facebook webhook verification secret"
    )
    instagram_webhook_secret: Optional[str] = Field(
        default=None,
        description="Instagram webhook verification secret"
    )

    # Notification services
    firebase_server_key: Optional[str] = Field(
        default=None,
        description="Firebase server key for push notifications"
    )
    sendgrid_api_key: Optional[str] = Field(
        default=None,
        description="SendGrid API key for email notifications"
    )
    twilio_account_sid: Optional[str] = Field(
        default=None,
        description="Twilio account SID"
    )
    twilio_auth_token: Optional[str] = Field(
        default=None,
        description="Twilio authentication token"
    )
    twilio_phone_number: Optional[str] = Field(
        default=None,
        description="Twilio phone number"
    )

    # AWS S3
    aws_access_key_id: Optional[str] = Field(
        default=None,
        description="AWS access key ID"
    )
    aws_secret_access_key: Optional[str] = Field(
        default=None,
        description="AWS secret access key"
    )
    s3_bucket_name: str = Field(
        default="omnilead-attachments",
        description="S3 bucket name for file storage"
    )

    # Environment
    environment: str = Field(
        default="development",
        description="Application environment (development, staging, production)"
    )
    debug: bool = Field(
        default=True,
        description="Debug mode"
    )

    @field_validator('secret_key')
    @classmethod
    def validate_secret_key(cls, v: str) -> str:
        """Warn if using default secret key in production"""
        if v == "your-secret-key-change-in-production" or v == "your-secret-key":
            import warnings
            warnings.warn(
                "Using default secret key! This is insecure. "
                "Please set SECRET_KEY environment variable in production.",
                UserWarning
            )
        return v

    @field_validator('database_url')
    @classmethod
    def validate_database_url(cls, v: str) -> str:
        """Validate database URL format"""
        if not v.startswith(('postgresql://', 'postgresql+psycopg2://', 'sqlite:///')):
            raise ValueError("Database URL must start with postgresql://, postgresql+psycopg2://, or sqlite:///")
        return v

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False
        # Allow reading from environment variables with these prefixes
        env_prefix = ""

# Validate settings on import
settings = Settings()

# Additional validation for production
if settings.environment == "production":
    if settings.secret_key in ["your-secret-key", "your-secret-key-change-in-production"]:
        raise ValueError(
            "SECRET_KEY must be set to a secure value in production! "
            "Generate one using: python -c 'import secrets; print(secrets.token_urlsafe(32))'"
        )
    if settings.debug:
        import warnings
        warnings.warn("Debug mode is enabled in production!", UserWarning)