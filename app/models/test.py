
from typing import Optional
from sqlmodel import Field
from models.base import BaseModel

class Test(BaseModel, table=True):
    __tablename__ = "test"

    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
