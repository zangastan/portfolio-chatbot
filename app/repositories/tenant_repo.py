from app.repositories.base import BaseRepository
from app.models.tenant import Tenant

class TenantRepository(BaseRepository[Tenant]):
    def __init__(self, client):
        super().__init__(client, "tenants", Tenant)
        
