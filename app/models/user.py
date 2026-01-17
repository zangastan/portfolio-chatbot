from datetime import datetime
from typing import Optional
from pydantic import BaseModel, UUID4, EmailStr, ConfigDict

class User(BaseModel):
    model_config = ConfigDict(extra='ignore')
    
    id: UUID4
    email: EmailStr
    role: str  # 'admin', 'agent'
    tenant_id: UUID4
    created_at: datetime

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    role: str = "agent"

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    role: Optional[str] = None
