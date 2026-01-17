from typing import Any, Dict, List, Optional, Type, TypeVar, Generic
from pydantic import BaseModel
from supabase import Client

T = TypeVar("T", bound=BaseModel)

class BaseRepository(Generic[T]):
    def __init__(self, client: Client, table: str, model: Type[T]):
        self.client = client
        self.table = table
        self.model = model

    def create(self, data: Dict[str, Any]) -> T:
        response = self.client.table(self.table).insert(data).execute()
        return self.model(**response.data[0])

    def get_by_id(self, id: str) -> Optional[T]:
        response = self.client.table(self.table).select("*").eq("id", id).execute()
        if not response.data:
            return None
        return self.model(**response.data[0])
    
    def update(self, id: str, data: Dict[str, Any]) -> T:
        response = self.client.table(self.table).update(data).eq("id", id).execute()
        if not response.data:
            raise ValueError(f"Entity with id {id} not found")
        return self.model(**response.data[0])

    def delete(self, id: str) -> bool:
        self.client.table(self.table).delete()\
            .eq("id", id)\
            .execute()
        return True

    def list_by_tenant(self, tenant_id: str, limit: int = 100, offset: int = 0) -> List[T]:
        response = self.client.table(self.table)\
            .select("*")\
            .eq("tenant_id", tenant_id)\
            .range(offset, offset + limit - 1)\
            .execute()
        return [self.model(**item) for item in response.data]
