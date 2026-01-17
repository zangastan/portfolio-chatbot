from pydantic import BaseModel
from typing import Dict, Any, Optional
from datetime import datetime

class AnalyticsEventBase(BaseModel):
    event_name: str
    properties: Dict[str, Any] = {}
    source: str = "web"

class AnalyticsEventCreate(AnalyticsEventBase):
    pass

class AnalyticsSummaryResponse(BaseModel):
    total_events: int
    period: str
    data: Dict[str, Any]
