from app.repositories.base import BaseRepository
from app.models.analytics import AnalyticsEvent

class AnalyticsRepository(BaseRepository[AnalyticsEvent]):
    def __init__(self, client):
        super().__init__(client, "analytics", AnalyticsEvent)
