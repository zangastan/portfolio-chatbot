from fastapi import APIRouter, Depends, HTTPException
from typing import Dict, Any
from app.services.tenant_service import TenantService
from app.core.dependencies import get_current_user
from app.models.tenant import Tenant

router = APIRouter(prefix="/tenants", tags=["tenants"])
tenant_service = TenantService()

@router.post("/", response_model=Tenant)
def create_tenant(payload: Dict[str, str], current_user: Any = Depends(get_current_user)):
    user_id = current_user.id
    email = current_user.email
    return tenant_service.create_tenant(payload.get("name"), admin_user_id=user_id, admin_email=email)

@router.get("/{tenant_id}", response_model=Tenant)
def get_tenant(tenant_id: str):
    tenant = tenant_service.get_tenant(tenant_id)
    if not tenant:
        raise HTTPException(status_code=404, detail="Tenant not found")
    return tenant
