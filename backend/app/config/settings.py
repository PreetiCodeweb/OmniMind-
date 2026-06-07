"""
Configuration management using Pydantic Settings.

Loads values from environment variables (or .env file).
Centralises all runtime config so nothing is hard-coded in business logic.
"""

from functools import lru_cache

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment."""

    PROJECT_NAME: str = "OmniMind Backend"
    VERSION: str = "0.1.0"
    API_PREFIX: str = "/api/v1"
    FRONTEND_URL: str = "http://localhost:5173"
    DEBUG: bool = False

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache()
def get_settings() -> Settings:
    """Return cached Settings instance (singleton)."""
    return Settings()
