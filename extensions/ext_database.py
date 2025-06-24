import os 

from fastapi import FastAPI
from sqlmodel import create_engine 
from sqlalchemy import QueuePool

from configs import config

def is_enabled() -> bool:
    return True 

def init_app(app: FastAPI):
    

    engine = create_engine(
        config.DATABASE_URL,
        pool_pre_ping=True,
        poolclass=QueuePool,
        pool_size=config.DATABASE_POOL_SIZE,
        max_overflow=config.DATABASE_MAX_OVERFLOW,
        pool_timeout=30,  # Connection timeout (seconds)
        pool_recycle=1800,  # Recycle connections after 30 minutes
    )

    app.state.engine = engine 

    