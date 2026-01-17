from app.schemas.knowledge import DocumentCreate, DocumentResponse
from typing import List

def create_document(data: DocumentCreate) -> DocumentResponse:
    return DocumentResponse(
        id="stub_doc_id",
        title=data.title,
        content=data.content,
        tags=data.tags,
        created_at="2023-01-01"
    )

def get_documents() -> List[DocumentResponse]:
    return []

def delete_document(id: str):
    return {"message": f"Document {id} deleted"}
