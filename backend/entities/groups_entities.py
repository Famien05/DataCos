from typing import Optional
from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from database import Base

class Group(Base):
    __tablename__ = "groups"

    id_group = Column(Integer, primary_key=True, index=True)
    group_name = Column(String(50), unique=True,nullable=False)
    tenant_name = Column(String, ForeignKey("tenants.tenant_name"), nullable=False)
    description = Column(String(255), nullable=False)

class GroupBase(BaseModel):
    group_name: str
    tenant_name: str
    description: str

class GroupInDB(GroupBase):
    id_group: int

    class Config:
        orm_mode = True

class GroupPublic(GroupInDB):
    pass
