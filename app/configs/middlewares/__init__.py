
from pydantic_settings import BaseSettings


class DatabaseConfig(BaseSettings):
    pass 


class MiddlewareConfig(
    DatabaseConfig    
):
    pass
