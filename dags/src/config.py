"""Configuration file to hold database connection data."""
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Pydantic BaseSettings"""
    staging_db: str = "staging"
    main_db: str = "airbnb"
    user: str = "postgres"
    password: str = "postgres"
    host: str = "localhost"
    port: int = 5432


def init_settings() -> None:
    global settings
    settings = Settings()


settings = None
if not settings:
    init_settings()
