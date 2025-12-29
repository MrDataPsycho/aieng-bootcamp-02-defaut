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
    
    Uses QDRANT_URL environment variable if set, otherwise defaults based on environment.
    - Docker: http://qdrant:6333
    - Local: http://localhost:6333
    
    Returns:
        The Qdrant service URL
    """
    # Check for explicit QDRANT_URL environment variable
    qdrant_url = os.getenv("QDRANT_URL")
    
    if qdrant_url:
        return qdrant_url
    
    # Check if running in Docker
    is_docker = os.getenv("DOCKER_ENV", "").lower() in ["true", "1", "yes"]
    
    if is_docker:
        return "http://qdrant:6333"
    
    # Default to localhost for local development
    return "http://localhost:6333"


# Qdrant configuration
QDRANT_URL = get_qdrant_url()
QDRANT_COLLECTION_NAME = "Amazon-items-collection-01-hybrid-search"

if __name__ == "__main__":
    print(config)