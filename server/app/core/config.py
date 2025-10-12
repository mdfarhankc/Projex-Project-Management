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
    
    # Database
    DATABASE_URI: str
    
    # Token
    

    # First Superuser Creds
    FIRST_SUPERUSER_NAME: str = "Administrator"
    FIRST_SUPERUSER_EMAIL: str = "admin@projex.com"
    FIRST_SUPERUSER_PASSWORD: str = "admin"


settings = Settings()
