
from pydantic import BaseModel
from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.ext.declarative import declarative_base
from database import Base

class Admin(Base):
    __tablename__ = "admins"

    id = Column(Integer, primary_key=True, index=True)
    uid_admin = Column(String(50), ForeignKey("users.uid_user"),unique=True, nullable=False)

class AdminBase(BaseModel):
    uid_admin: str

class AdminInDB(AdminBase):
    id: int

    class Config:
        orm_mode = True

class AdminPublic(AdminInDB):
    pass
