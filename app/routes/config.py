from fastapi import APIRouter, Depends, HTTPException
from typing import Optional
from app.services.config_service import ConfigService
from app.models.config import ConfigStyles, NewConfig
from app.core.dependencies import get_current_tenant

router = APIRouter(prefix="/config", tags=["config"])
service = ConfigService()

@router.get("/", response_model=ConfigStyles)
async def get_config(
    tenant_id: str = Depends(get_current_tenant)
):
    """
    Get chatbot configuration/styles for the current tenant.
    Returns the customization settings including name, greeting, theme, etc.
    """
    config = await service.get_config(tenant_id)
    if not config:
        raise HTTPException(
            status_code=404, 
            detail="Config not found for this tenant. Please create one first."
        )
    return config

@router.put("/", response_model=ConfigStyles)
async def save_config(
    data: NewConfig,
    tenant_id: str = Depends(get_current_tenant)
):
    """
    Save or update chatbot configuration/styles for the current tenant.
    Creates a new config if none exists, or updates the existing one.
    """
    config = await service.save_config(tenant_id, data)
    return config

