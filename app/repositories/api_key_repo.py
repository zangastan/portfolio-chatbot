from typing import Optional
from app.repositories.base import BaseRepository
from app.models.api_key import APIKey
from datetime import datetime

class APIKeyRepository(BaseRepository[APIKey]):
    def __init__(self, client):
        super().__init__(client, "api_keys", APIKey)

    def get_by_prefix(self, prefix: str) -> Optional[APIKey]:
        response = self.client.table(self.table)\
            .select("*")\
            .eq("prefix", prefix)\
            .execute()
        if not response.data:
            return None
        return self.model(**response.data[0])

    def update_last_used(self, key_id: str):
        self.client.table(self.table)\
            .update({"last_used_at": datetime.utcnow().isoformat()})\
            .eq("id", key_id)\
            .execute()
