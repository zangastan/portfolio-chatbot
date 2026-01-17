from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, UUID4, ConfigDict

class KnowledgeEmbedding(BaseModel):
    model_config = ConfigDict(extra='ignore')
    
    id: UUID4
    document_id: UUID4
    tenant_id: UUID4
    content_chunk: str
    chunk_index: int
    embedding: List[float]  # Vector
    created_at: datetime

class KnowledgeEmbeddingCreate(BaseModel):
    document_id: UUID4
    content_chunk: str
    chunk_index: int
    embedding: List[float]
