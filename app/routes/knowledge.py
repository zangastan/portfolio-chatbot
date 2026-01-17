from fastapi import APIRouter, Depends, UploadFile, File, Form
from typing import List, Optional
from uuid import UUID
from app.services.knowledge_service import KnowledgeService
from app.models.knowledge import KnowledgeDocument, KnowledgeDocumentCreate
from app.core.dependencies import get_current_tenant

router = APIRouter(prefix="/knowledge", tags=["knowledge"])
service = KnowledgeService()

@router.post("/", response_model=KnowledgeDocument)
def add_document(
    data: KnowledgeDocumentCreate,
    tenant_id: str = Depends(get_current_tenant)
):
    return service.add_document(tenant_id, data.title, data.content)

@router.post("/upload", response_model=KnowledgeDocument)
async def upload_document(
    file: UploadFile = File(...),
    title: Optional[str] = Form(None),
    tenant_id: str = Depends(get_current_tenant)
):
    return await service.ingest_file(tenant_id, file, title)

@router.delete("/delete/{doc_id}")
def delete_document(
    doc_id: UUID,
    # tenant_id: str = Depends(get_current_tenant)
):
    print(doc_id)
    service.delete_document(str(doc_id))
    return {"status": "success", "message": "Document deleted"}

@router.get("/", response_model=List[KnowledgeDocument])
def list_documents(tenant_id: str = Depends(get_current_tenant)):
    return service.get_tenant_documents(tenant_id)
