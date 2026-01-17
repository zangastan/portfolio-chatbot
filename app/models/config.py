from datetime import datetime
from typing import Optional, Any
from pydantic import BaseModel, UUID4, ConfigDict

class ConfigBase(BaseModel):
    model_config = ConfigDict(extra='ignore')


class ConfigStyles(BaseModel):
    """Response model with tenant_id for API responses"""
    tenant_id: str
    name: str
    greeting_msg: str
    rounded: bool
    theme: Optional[dict] = None

class NewConfig(BaseModel):
    """Request model for creating/updating config (no tenant_id needed)"""
    name: str
    greeting_msg: str
    rounded: bool
    theme: Optional[dict] = None

class Config(ConfigBase):
    """Full config model with database metadata"""
    id: str
    tenant_id: str
    name: str
    greeting_msg: str
    rounded: bool
    theme: Optional[dict] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

