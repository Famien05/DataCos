from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from entities.admins_entities import AdminBase, AdminPublic, Admin

admin_router = APIRouter()
from entities.users_entities import User

@admin_router.post("/", response_model=AdminPublic)
async def create_admin(admin: AdminBase, db: Session = Depends(get_db)):
    # Vérifiez si l'utilisateur existe
    db_user = db.query(User).filter(User.uid_user == admin.uid_admin).first()
    if not db_user:
        raise HTTPException(status_code=400, detail="User UID not found")
    
    db_admin = Admin(**admin.dict())
    db.add(db_admin)
    db.commit()
    db.refresh(db_admin)
    return db_admin



@admin_router.get("/", response_model=List[AdminPublic])
async def get_admins(db: Session = Depends(get_db)):
    admins = db.query(Admin).all()
    return admins
