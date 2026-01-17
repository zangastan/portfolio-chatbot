from fastapi import APIRouter, Depends
from typing import List
from app.services.analytics_service import AnalyticsService
from app.models.analytics import AnalyticsEvent
from app.core.dependencies import get_current_tenant

router = APIRouter(prefix="/analytics", tags=["analytics"])
service = AnalyticsService()

@router.get("/events", response_model=List[AnalyticsEvent])
def get_events(tenant_id: str = Depends(get_current_tenant)):
    return service.get_tenant_analytics(tenant_id)
