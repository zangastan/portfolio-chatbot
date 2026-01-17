from datetime import datetime
from typing import Optional
from pydantic import BaseModel, UUID4, ConfigDict

class Message(BaseModel):
    model_config = ConfigDict(extra='ignore')
    content: str
    created_at: datetime
    metadata: Optional[dict] = None

class MessageCreate(BaseModel):
    # conversation_id: UUID4
    # sender_type: str
    content: str
    metadata: Optional[dict] = None

class MessageResponse(BaseModel):
    user_message: Message
    ai_message: Optional[Message] = None
