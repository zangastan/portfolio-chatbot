from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from uuid import UUID

class APIKeyRequest(BaseModel):
    name: str
    scopes: List[str] = []

class APIKeyResponse(BaseModel):
    id: UUID
    name: str
    prefix: str
    scopes: List[str]
    is_active: bool
    created_at: datetime
    last_used_at: Optional[datetime]
    
    class Config:
        from_attributes = True

class APIKeyCreateResponse(APIKeyResponse):
    secret_key: str  # Only returned once on creation
