from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import users_routers, admins_routers, tenants_routers, groups_routers, licenses_routers

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Vous pouvez spécifier les origines spécifiques ici
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users_routers.router, prefix="/users", tags=["users"])
app.include_router(admins_routers.admin_router, prefix="/admins", tags=["admins"])
app.include_router(tenants_routers.tenant_router, prefix="/tenants", tags=["tenants"])
app.include_router(groups_routers.group_router, prefix="/groups", tags=["groups"])
app.include_router(licenses_routers.license_router, prefix="/licenses", tags=["licenses"])
