from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from entities.relations_entities import User_Groups, Add_User_Requests
from entities.users_entities import UserBase, UserPublic, User
from datetime import date
from entities.tenants_entities import Tenant
from entities.groups_entities import Group
from entities.licenses_entities import License


from database import get_db

router = APIRouter()

@router.post("/", response_model=UserPublic)
async def create_user(user: UserBase, db: Session = Depends(get_db)):
    db_user = User(**user.dict())  # Créez une instance d'utilisateur à partir des données de la requête
    db.add(db_user)  # Ajoutez l'utilisateur à la session
    db.commit()  # Validez les changements
    db.refresh(db_user)  # Actualisez l'instance avec les données de la base de données (comme l'ID généré)
    return db_user  # Retournez l'utilisateur créé

@router.get("/", response_model=List[UserPublic])
async def get_users(db: Session = Depends(get_db)):
    users = db.query(User).all()  # Récupérez tous les utilisateurs
    return users


def create_user_and_add_to_group(user: UserBase, group_id: int, tenant: Tenant, db: Session):
    new_user = User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    user_group = User_Groups(user_id=new_user.id, group_id=group_id, added_date=date.today())
    db.add(user_group)

    add_user_request = Add_User_Requests(uid_admin=tenant.uid_admin, uid_user=new_user.uid_user, tenant_id=tenant.id_tenant, group_id=group_id, request_date=date.today(), status="Added")
    db.add(add_user_request)

    db.commit()
    return new_user

"""
@router.post("/add_to_tenant/{tenant_id}/group/{group_id}", response_model=UserPublic)
async def add_user_to_tenant(tenant_id: int, group_id: int, user: UserBase, db: Session = Depends(get_db)):
    # Vérification du tenant
    tenant = db.query(Tenant).filter_by(id_tenant=tenant_id).first()
    if not tenant:
        raise HTTPException(status_code=404, detail="Tenant not found")

    # Vérification du groupe
    group = db.query(Group).filter_by(id_group=group_id, tenant_id=tenant_id).first()
    if not group:
        raise HTTPException(status_code=404, detail="Group not found")

    # Si le profil est "Designer", vérifiez les licences
    if user.profile == "Designer":
        license = db.query(License).filter_by(tenant_id=tenant_id, is_active=True).first()
        if not license or license.license_count <= 0:
            raise HTTPException(status_code=400, detail="No licenses available for Designer profile")
        license.license_count -= 1  # Diminuer le nombre de licences disponibles

    # Si le profil est "Reader", continuez avec la création
    if user.profile == "Reader":
        new_user = User(**user.dict())
        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        # Ajouter l'utilisateur au groupe
        user_group = User_Groups(user_id=new_user.id, group_id=group_id, added_date=date.today())
        db.add(user_group)

        # Ajouter une entrée dans Add_User_Requests
        add_user_request = Add_User_Requests(uid_admin=tenant.uid_admin, uid_user=new_user.uid_user, tenant_id=tenant_id, group_id=group_id, request_date=date.today(), status="Added")
        db.add(add_user_request)

        db.commit()
        return new_user  # Retournez l'utilisateur créé
"""
@router.post("/add_to_tenant/{tenant_id}/group/{group_id}", response_model=UserPublic)
async def add_user_to_tenant(tenant_id: int, group_id: int, user: UserBase, db: Session = Depends(get_db)):
    tenant = db.query(Tenant).filter_by(id_tenant=tenant_id).first()
    if not tenant:
        raise HTTPException(status_code=404, detail="Tenant not found")

    group = db.query(Group).filter_by(id_group=group_id, tenant_id=tenant_id).first()
    if not group:
        raise HTTPException(status_code=404, detail="Group not found")

    if user.profile == "Reader":
        return create_user_and_add_to_group(user, group_id, tenant, db)
    elif user.profile == "Designer":
        license = db.query(License).filter_by(tenant_id=tenant_id, is_active=True).first()
        if not license or license.license_count <= 0:
            raise HTTPException(status_code=400, detail="No licenses available for Designer profile")
        license.license_count -= 1
        return create_user_and_add_to_group(user, group_id, tenant, db)