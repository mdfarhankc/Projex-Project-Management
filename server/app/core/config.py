from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file="./.env",
        env_ignore_empty=True,
        extra="ignore",
        case_sensitive=True,
    )

    # Project Details
    PROJECT_NAME: str = "Projex Server"
    PROJECT_DESCRIPTION: str = "Server for the projex flutter app."
    PROJECT_VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    RELOAD: bool = False

    # Server
    TOKEN_SECRET_KEY: str
    TOKEN_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30  # 30 minutes
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7  # 7 days

    # Database
    DATABASE_URL: str
    
    # Redis
    REDIS_URL: str

    # First Superuser Creds
    FIRST_SUPERUSER_NAME: str = "Administrator"
    FIRST_SUPERUSER_EMAIL: str = "admin@projex.com"
    FIRST_SUPERUSER_PASSWORD: str = "admin"


settings = Settings()
