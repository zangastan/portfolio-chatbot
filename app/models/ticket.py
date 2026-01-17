from datetime import datetime
from typing import Optional
from pydantic import BaseModel, UUID4, ConfigDict

class Ticket(BaseModel):
    model_config = ConfigDict(extra='ignore')

    id: UUID4
    tenant_id: UUID4
    conversation_id: UUID4
    status: str = "open" # open, in_progress, resolved, closed
    priority: str = "medium" # low, medium, high, urgent
    created_at: datetime
    description: Optional[str] = None

class TicketCreate(BaseModel):
    conversation_id: UUID4
    priority: str = "medium"
    description: Optional[str] = None

class TicketUpdate(BaseModel):
    status: Optional[str] = None
    priority: Optional[str] = None
