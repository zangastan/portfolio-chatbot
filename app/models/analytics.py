from datetime import datetime
from typing import Optional, Any
from pydantic import BaseModel, UUID4, ConfigDict

class AnalyticsEvent(BaseModel):
    model_config = ConfigDict(extra='ignore')

    id: UUID4
    tenant_id: UUID4
    event_type: str # message_sent, conversation_started, ticket_created
    data: Optional[dict] = None
    created_at: datetime

class AnalyticsEventCreate(BaseModel):
    event_type: str
    data: Optional[dict] = None
