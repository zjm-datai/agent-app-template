from pydantic_settings import BaseSettings
from pydantic import Field, NonNegativeInt, SecretStr, HttpUrl


class DatabaseConfig(BaseSettings):

    DATABASE_URL: str = Field(
        description="",
        default=""
    )

    DATABASE_POOL_SIZE: NonNegativeInt = Field(
        description="",
        default=20,    
    )

    DATABASE_MAX_OVERFLOW: NonNegativeInt = Field(
        description="", 
        default=10
    )

class LLMConfig(BaseSettings):
    """
    Configuration for the language model client.
    Reads values from environment variables or a .env file.
    """
    
    LLM_MODEL: str = Field(
        "gpt-4o",
        env="LLM_MODEL",
        description="Name of the LLM to use (e.g. 'gpt-4o', 'gpt-3.5-turbo')"
    )
    DEFAULT_LLM_TEMPERATURE: float = Field(
        0.7,
        env="DEFAULT_LLM_TEMPERATURE",
        description="Sampling temperature for the LLM",
        ge=0.0,
        le=2.0
    )
    LLM_API_KEY: SecretStr = Field(
        ...,
        env="LLM_API_KEY",
        description="API key for accessing the LLM service"
    )
    LLM_BASE_URL: HttpUrl = Field(
        "https://api.openai.com/v1",
        env="LLM_BASE_URL",
        description="Base URL for the LLM HTTP API"
    )
    MAX_TOKENS: NonNegativeInt = Field(
        2048,
        env="MAX_TOKENS",
        description="Maximum number of tokens to generate per call",
        ge=0
    )

class MiddlewareConfig(
    DatabaseConfig,
    LLMConfig    
):
    pass