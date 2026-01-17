from datetime import datetime
from typing import Optional, Dict, Any
from pydantic import BaseModel, UUID4, Field, ConfigDict

class Tenant(BaseModel):
    model_config = ConfigDict(extra='ignore')
    
    id: UUID4
    name: str
    created_at: datetime
    config: Dict[str, Any] = Field(default_factory=dict)

class TenantCreate(BaseModel):
    name: str
    config: Optional[Dict[str, Any]] = None

class TenantUpdate(BaseModel):
    name: Optional[str] = None
    config: Optional[Dict[str, Any]] = None
