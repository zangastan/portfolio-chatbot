from datetime import datetime
from typing import Optional
from pydantic import BaseModel, UUID4, ConfigDict

class Conversation(BaseModel):
    model_config = ConfigDict(extra='ignore')

    id: UUID4
    tenant_id: UUID4
    visitor_id: Optional[str] = None # Can be UUID or session string
    status: str = "open" # open, in_progress, waiting, closed
    assigned_agent_id: Optional[UUID4] = None
    created_at: datetime
    updated_at: datetime

class ConversationCreate(BaseModel):
    visitor_id: str
    status: str = "open"

class ConversationUpdate(BaseModel):
    status: Optional[str] = None
    assigned_agent_id: Optional[UUID4] = None
