from typing import Optional
from pydantic import BaseModel
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    uid_user = Column(String, unique=True, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    profile = Column(String, nullable=False)
    
class UserBase(BaseModel):
    uid_user: str
    first_name: str
    last_name: str
    email: str
    profile: str

class UserInDB(UserBase):
    id: int

    class Config:
        orm_mode = True

class UserPublic(UserInDB):
    pass
