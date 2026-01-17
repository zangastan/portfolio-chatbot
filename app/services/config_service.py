from datetime import datetime
from typing import List, Optional
from app.repositories.config_repo import ConfigRepo
from app.models.config import ConfigStyles, NewConfig
from app.core.database import supabase

class ConfigService:
    def __init__(self):
        self.repo = ConfigRepo(supabase)

    async def get_config(self, tenant_id: str) -> Optional[ConfigStyles]:
        """Get chatbot configuration for a tenant"""
        return self.repo.get_config(tenant_id)
    
    async def save_config(self, tenant_id: str, config: NewConfig) -> ConfigStyles:
        """Save or update chatbot configuration for a tenant"""
        config_data = config.model_dump()
        return self.repo.save_config(tenant_id, config_data)
