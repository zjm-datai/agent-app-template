
from typing import Optional
from sqlmodel import Field, Relationship, SQLModel, select
from models.base import BaseModel

class User(BaseModel, table=True):
    __tablename__ = "user" 

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    email: str

    items: list["Item"] = Relationship(back_populates="owner")


class Item(BaseModel, table=True):
    __tablename__ = "item"

    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    owner_id: int = Field(foreign_key="user.id")
    owner: Optional[User] = Relationship(back_populates="items")

class Items(BaseModel, table=True):
    __tablename__ = "items"

    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
