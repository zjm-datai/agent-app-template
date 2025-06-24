from pydantic_settings import BaseSettings
from pydantic import Field, NonNegativeInt


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

class MiddlewareConfig(
    DatabaseConfig    
):
    pass