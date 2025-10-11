"""Configuration management using Pydantic Settings."""

from pydantic import config
from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    """Application settings loaded from environment variables."""
    OPENAI_API_KEY: str
    BACKEND_API_URL: str = "http://localhost:8000"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )


# Global settings instance
config = Config()

if __name__ == "__main__":
    print(config)