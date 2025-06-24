""" 
Application configuration management 

This module handles environment-specific configuration loading, parsing, and management
for the application. It includes environment detection, .env file loading, and
configuration value parsing.
"""

import os
from pathlib import Path
from enum import Enum

from pydantic_settings import SettingsConfigDict

from .middlewares import MiddlewareConfig


# Define environment types 
class Environment(str, Enum):

    DEVELOPMENT = "development"
    STAGING = "staging"
    PRODUCTION = "production"
    TEST = "test"

def get_environment() -> Environment:
    """Detect current env from APP_ENV var."""
    raw = os.getenv("APP_ENV", "development").lower()
    match raw:
        case "production" | "prod":
            return Environment.PRODUCTION
        case "staging" | "stage":
            return Environment.STAGING
        case "test":
            return Environment.TEST
        case _:
            return Environment.DEVELOPMENT

# Prepare prioritized env files list
_env = get_environment()
base_dir = Path(__file__).resolve().parent.parent.parent
# print(base_dir)
env_files = [
    base_dir / f".env.{_env.value}.local",
    base_dir / f".env.{_env.value}",
    base_dir / ".env.local",
    base_dir / ".env",
]
# Tell pydantic to load env files in order

class Settings(
    MiddlewareConfig
):
    model_config = SettingsConfigDict(
        env_file=[str(path) for path in env_files],
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    