from pydantic import BaseModel
from typing import Optional, List

class DocumentBase(BaseModel):
    title: str
    content: str
    tags: List[str] = []

class DocumentCreate(DocumentBase):
    pass

class DocumentResponse(DocumentBase):
    id: str
    created_at: str

    class Config:
        from_attributes = True
