from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class TicketBase(BaseModel):
    title: str
    description: Optional[str] = None
    priority: str = "medium"

class TicketCreate(TicketBase):
    pass

class TicketUpdate(BaseModel):
    status: str

class TicketResponse(TicketBase):
    id: str
    status: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
