from datetime import datetime
from typing import Dict, Any, List
from app.repositories.analytics_repo import AnalyticsRepository
from app.models.analytics import AnalyticsEvent
from app.core.database import supabase

class AnalyticsService:
    def __init__(self):
        self.repo = AnalyticsRepository(supabase)

    def track_event(self, tenant_id: str, event_type: str, data: Dict[str, Any] = None):
        return self.repo.create({
            "tenant_id": tenant_id,
            "event_type": event_type,
            "data": data or {},
            "created_at": datetime.utcnow().isoformat()
        })

    def get_tenant_analytics(self, tenant_id: str) -> List[AnalyticsEvent]:
        # Return raw events for now. Aggregation can happen here or in DB.
        return self.repo.list_by_tenant(tenant_id)
