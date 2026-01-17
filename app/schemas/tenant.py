from pydantic import BaseModel
from typing import Optional, List

class TenantBase(BaseModel):
    name: str
    domain: Optional[str] = None
    plan: str = "free"

class TenantCreate(TenantBase):
    pass

class TenantUpdate(TenantBase):
    name: Optional[str] = None
    plan: Optional[str] = None

class TenantResponse(TenantBase):
    id: str
    created_at: str

    class Config:
        from_attributes = True

class TenantSettingsUpdate(BaseModel):
    theme: Optional[str] = None
    notifications_enabled: Optional[bool] = None
