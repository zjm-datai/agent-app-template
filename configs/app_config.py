""" Application configuration management 
"""

from pydantic_settings import SettingsConfigDict
from .middleware import MiddlewareConfig


# Tell pydantic to load env files in order
class AppConfig(
    MiddlewareConfig
):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    