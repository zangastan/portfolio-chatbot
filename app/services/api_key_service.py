import secrets
from datetime import datetime
from typing import Optional, Tuple
from app.core.security import pwd_context
from app.repositories.api_key_repo import APIKeyRepository
from app.core.database import supabase
from app.models.api_key import APIKey

class APIKeyService:
    def __init__(self):
        self.repo = APIKeyRepository(supabase)

    def create_key(self, user_id: str, name: str, scopes: list[str] = []) -> Tuple[APIKey, str]:
        """
        Creates a new API key.
        Returns the APIKey object and the raw secret key (which is shown ONLY ONCE).
        """
        # Generate secure random key
        raw_token = secrets.token_urlsafe(32)
        prefix = f"ico_{raw_token[:8]}"
        full_key = f"ico_{raw_token}"
        
        # Hash the key (Bcrypt limit is 72 bytes)
        key_hash = pwd_context.hash(full_key[:72])
        
        # Store metadata and hash
        api_key = self.repo.create({
            "user_id": user_id,
            "name": name,
            "prefix": prefix,
            "key_hash": key_hash,
            "scopes": scopes,
            "is_active": True,
            "created_at": datetime.utcnow().isoformat()
        })
        
        return api_key, full_key

    def validate_key(self, api_key_header: str) -> Optional[APIKey]:
        """
        Validates an API key from a request header.
        expects key format: "ico_..."
        """
        if not api_key_header.startswith("ico_"):
            return None
            
        # Extract prefix (first 12 chars: "ico_" + 8 chars)
        # Actually in create_key I did prefix = "ico_" + raw[:8]
        # full_key = "ico_" + raw
        # so prefix is first 12 chars of the full key (4 for "ico_" + 8 from raw)
        
        if len(api_key_header) < 12:
            return None
            
        prefix = api_key_header[:12]
        
        key_record = self.repo.get_by_prefix(prefix)
        if not key_record:
            return None
            
        if not key_record.is_active:
            return None
            
        if key_record.expires_at and key_record.expires_at < datetime.utcnow():
            return None
            
        # Verify hash (Truncate to 72 bytes to match Bcrypt limit handled during creation)
        if not pwd_context.verify(api_key_header[:72], key_record.key_hash):
            return None
            
        # Update usage stats (async side effect ideally, but sync here for now)
        self.repo.update_last_used(str(key_record.id))
        
        return key_record

    def revoke_key(self, key_id: str, user_id: str) -> bool:
        """
        Revokes (deletes or deactivates) a key.
        Checks ownership.
        """
        key = self.repo.get_by_id(key_id)
        if not key or str(key.user_id) != user_id:
            return False
            
        self.repo.delete(key_id)
        return True

    def list_keys(self, user_id: str) -> list[APIKey]:
        # Filter by user_id manually since repo.list_by_tenant uses tenant_id
        # Ideally repo should have list_by_user
        response = self.repo.client.table(self.repo.table)\
            .select("*")\
            .eq("user_id", user_id)\
            .execute()
        return [self.repo.model(**item) for item in response.data]
