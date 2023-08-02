from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import date
from database import get_db
from entities.tenants_entities import TenantBase, TenantPublic, Tenant
from entities.admins_entities import Admin

tenant_router = APIRouter()

@tenant_router.post("/", response_model=TenantPublic)
async def create_tenant(tenant: TenantBase, db: Session = Depends(get_db)):
    # Vérifiez si l'uid_admin est valide (maintenant toujours présent)
    db_admin = db.query(Admin).filter(Admin.uid_admin == tenant.uid_admin).first()
    if not db_admin:
        raise HTTPException(status_code=400, detail="Admin ID not found")
    
    db_tenant = Tenant(**tenant.dict(), created_date=date.today())
    db.add(db_tenant)
    db.commit()
    db.refresh(db_tenant)
    return db_tenant


@tenant_router.get("/", response_model=List[TenantPublic])
async def get_tenants(db: Session = Depends(get_db)):
    tenants = db.query(Tenant).all()
    return tenants
