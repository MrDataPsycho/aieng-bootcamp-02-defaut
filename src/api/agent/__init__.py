"""Agent module initialization."""
from dotenv import load_dotenv
from loguru import logger

# Load environment variables before any other imports
load_dotenv(override=True)
logger.info("Environment variables loaded successfully from .env file")
