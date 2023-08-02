from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from database import get_db
from entities.groups_entities import GroupBase, GroupPublic, Group
from entities.tenants_entities import Tenant

group_router = APIRouter()

@group_router.post("/", response_model=GroupPublic)
async def create_group(group: GroupBase, db: Session = Depends(get_db)):
    # Vérifiez si le tenant_id est valide
    db_tenant = db.query(Tenant).filter(Tenant.id_tenant == group.tenant_id).first()
    if not db_tenant:
        raise HTTPException(status_code=400, detail="Tenant ID not found")
    
    db_group = Group(**group.dict())
    db.add(db_group)
    db.commit()
    db.refresh(db_group)
    return db_group

@group_router.get("/", response_model=List[GroupPublic])
async def get_groups(db: Session = Depends(get_db)):
    groups = db.query(Group).all()
    return groups
