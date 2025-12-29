"""Configuration management using Pydantic Settings."""

import os
from pydantic import config
from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    """Application settings loaded from environment variables."""
    OPENAI_API_KEY: str
    GROQ_API_KEY: str
    GOOGLE_API_KEY: str

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )


# Global settings instance
config = Config()


def get_qdrant_url() -> str:
    """
    Get the Qdrant URL based on the environment.
    
    Uses QDRANT_URL environment variable if set, otherwise defaults to localhost.
    Set QDRANT_URL in docker-compose.yaml or .env file as needed.
    
    Returns:
        The Qdrant service URL (default: http://localhost:6333)
    """
    return os.getenv("QDRANT_URL", "http://localhost:6333")


# Qdrant configuration
QDRANT_URL = get_qdrant_url()
QDRANT_COLLECTION_NAME = "Amazon-items-collection-01-hybrid-search"

if __name__ == "__main__":
    print(config)