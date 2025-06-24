from sqlalchemy
from sqlalchemy.pool import QueuePool 
from sqlmodel import create_engine 

from app.core.config import settings 


class BaseDatabaseService:
    """ 
    A general database service base class responsible for engine initialization and session management
    """

        