from typing import Optional
from pydantic import BaseModel
from sqlalchemy import Column, Integer, Date, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from datetime import date
from database import Base

class License(Base):
    __tablename__ = "licenses"

    id_license = Column(Integer, primary_key=True, index=True)
    tenant_id = Column(Integer, ForeignKey("tenants.id_tenant"), nullable=False)
    license_count = Column(Integer, nullable=False)
    purchase_date = Column(Date, nullable=False) # Supprimé l'Optional
    expiration_date = Column(Date, nullable=False) # Supprimé l'Optional
    is_active = Column(Boolean, default=True)

class LicenseBase(BaseModel):
    tenant_id: int
    license_count: int
    purchase_date: date # Supprimé l'Optional
    expiration_date: date # Supprimé l'Optional
    is_active: Optional[bool] = True

class LicenseInDB(LicenseBase):
    id_license: int

    class Config:
        orm_mode = True

class LicensePublic(LicenseInDB):
    pass
