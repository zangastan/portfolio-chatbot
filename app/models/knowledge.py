from datetime import datetime
from typing import Optional
from pydantic import BaseModel, UUID4, ConfigDict

class KnowledgeDocument(BaseModel):
    model_config = ConfigDict(extra='ignore')

    id: UUID4
    tenant_id: UUID4
    title: str
    content: str
    created_at: datetime
    metadata: Optional[dict] = None

class KnowledgeDocumentCreate(BaseModel):
    title: str
    content: str
    metadata: Optional[dict] = None
