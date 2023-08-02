from typing import Optional
from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from datetime import date
from database import Base

class Tenant(Base):
    __tablename__ = "tenants"

    id_tenant = Column(Integer, primary_key=True, index=True)
    tenant_name = Column(String, nullable=False)
    uid_admin = Column(String, ForeignKey("admins.uid_admin"), nullable=False)
    created_date = Column(Date)

class TenantBase(BaseModel):
    tenant_name: str
    uid_admin: str

class TenantInDB(TenantBase):
    id_tenant: int
    created_date: date

    class Config:
        orm_mode = True

class TenantPublic(TenantInDB):
    pass
