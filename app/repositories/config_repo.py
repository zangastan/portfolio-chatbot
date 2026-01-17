from typing import List, Optional, Dict, Any
from app.repositories.base import BaseRepository
from app.models.config import ConfigStyles

class ConfigRepo(BaseRepository[ConfigStyles]):
    def __init__(self, client):
        super().__init__(client, "config", ConfigStyles)
    
    def get_config(self, tenant_id: str) -> Optional[ConfigStyles]:
        """Get config for a specific tenant"""
        response = self.client.table(self.table)\
            .select("*")\
            .eq("tenant_id", tenant_id)\
            .execute()
        
        if not response.data or len(response.data) == 0:
            return None
        return self.model(**response.data[0])
    
    def save_config(self, tenant_id: str, config_data: Dict[str, Any]) -> ConfigStyles:
        """Save or update config for a tenant using upsert"""
        # First check if config exists
        existing = self.get_config(tenant_id)
        
        # Prepare data with tenant_id
        data = {**config_data, "tenant_id": tenant_id}
        
        if existing:
            # Update existing config
            response = self.client.table(self.table)\
                .update(data)\
                .eq("tenant_id", tenant_id)\
                .execute()
        else:
            # Insert new config
            response = self.client.table(self.table)\
                .insert(data)\
                .execute()
        
        if not response.data:
            raise ValueError(f"Failed to save config for tenant {tenant_id}")
        
        return self.model(**response.data[0])

