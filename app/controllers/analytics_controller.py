from app.schemas.analytics import AnalyticsEventCreate, AnalyticsSummaryResponse

def track_event(data: AnalyticsEventCreate):
    return {"status": "recorded"}

def get_summary() -> AnalyticsSummaryResponse:
    return AnalyticsSummaryResponse(
        total_events=100,
        period="last_24h",
        data={"page_views": 50, "clicks": 50}
    )
