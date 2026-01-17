from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class MessageBase(BaseModel):
    content: str
    # sender_type: str  # user, agent, bot

class MessageCreate(MessageBase):
    # conversation_id: str

class MessageResponse(MessageBase):
    id: str
    timestamp: datetime

    class Config:
        from_attributes = True
