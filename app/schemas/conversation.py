from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class ConversationBase(BaseModel):
    subject: Optional[str] = None
    status: str = "open"

class ConversationCreate(ConversationBase):
    customer_id: str

class ConversationUpdate(BaseModel):
    status: Optional[str] = None
    assigned_agent_id: Optional[int] = None

class ConversationResponse(ConversationBase):
    id: str
    created_at: datetime
    assigned_agent_id: Optional[int] = None

    class Config:
        from_attributes = True

class AssignAgentRequest(BaseModel):
    agent_id: int
