from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from database import get_db
from entities.licenses_entities import LicenseBase, LicensePublic, License
from entities.tenants_entities import Tenant

license_router = APIRouter()

@license_router.post("/", response_model=LicensePublic)
async def create_license(license: LicenseBase, db: Session = Depends(get_db)):
    # Vérifiez si le tenant_id est valide
    db_tenant = db.query(Tenant).filter(Tenant.id_tenant == license.tenant_id).first()
    if not db_tenant:
        raise HTTPException(status_code=400, detail="Tenant ID not found")

    db_license = License(**license.dict())
    db.add(db_license)
    db.commit()
    db.refresh(db_license)
    return db_license

@license_router.get("/", response_model=List[LicensePublic])
async def get_licenses(db: Session = Depends(get_db)):
    licenses = db.query(License).all()
    return licenses

@license_router.get("/{license_id}", response_model=LicensePublic)
async def get_license(license_id: int, db: Session = Depends(get_db)):
    license = db.query(License).filter(License.id_license == license_id).first()
    if license is None:
        raise HTTPException(status_code=404, detail="License not found")
    return license

@license_router.put("/{license_id}", response_model=LicensePublic)
async def update_license(license_id: int, license: LicenseBase, db: Session = Depends(get_db)):
    db_license = db.query(License).filter(License.id_license == license_id).first()
    if db_license is None:
        raise HTTPException(status_code=404, detail="License not found")

    for key, value in license.dict().items():
        setattr(db_license, key, value)

    db.commit()
    db.refresh(db_license)
    return db_license
