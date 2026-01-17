from datetime import datetime
from typing import Optional, List, Any
from pydantic import BaseModel, UUID4, ConfigDict

class APIKeyBase(BaseModel):
    name: str
    scopes: Optional[List[str]] = []
    expires_at: Optional[datetime] = None
    is_active: bool = True

class APIKeyCreate(APIKeyBase):
    user_id: UUID4

class APIKey(APIKeyBase):
    model_config = ConfigDict(extra='ignore')
    
    id: UUID4
    user_id: UUID4
    prefix: str
    key_hash: str
    last_used_at: Optional[datetime] = None
    created_at: datetime
    
class APIKeyResponse(APIKeyBase):
    id: UUID4
    prefix: str
    created_at: datetime
    last_used_at: Optional[datetime] = None
