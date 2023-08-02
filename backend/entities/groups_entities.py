from typing import Optional
from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from database import Base

class Group(Base):
    __tablename__ = "groups"

    id_group = Column(Integer, primary_key=True, index=True)
    group_name = Column(String(50), nullable=False) # Longueur ajoutée
    tenant_id = Column(Integer, ForeignKey("tenants.id_tenant"), nullable=False)
    description = Column(String(255), nullable=False) # Supprimé l'Optional

class GroupBase(BaseModel):
    group_name: str
    tenant_id: int
    description: str # Supprimé l'Optional

class GroupInDB(GroupBase):
    id_group: int

    class Config:
        orm_mode = True

class GroupPublic(GroupInDB):
    pass
