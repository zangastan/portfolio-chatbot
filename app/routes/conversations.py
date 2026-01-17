from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Dict
from app.services.conversation_service import ConversationService
from app.models.conversation import Conversation, ConversationCreate, ConversationUpdate
from app.core.dependencies import get_current_tenant

router = APIRouter(prefix="/conversations", tags=["conversations"])
service = ConversationService()

@router.post("/", response_model=Conversation)
def create_conversation(
    data: ConversationCreate,
    tenant_id: str = Depends(get_current_tenant)
):
    return service.create_conversation(tenant_id, data.visitor_id)

@router.get("/", response_model=List[Conversation])
def list_conversations(
    tenant_id: str = Depends(get_current_tenant)
):
    return service.list_conversations(tenant_id)

@router.get("/{conversation_id}", response_model=Conversation)
def get_conversation(
    conversation_id: str,
    tenant_id: str = Depends(get_current_tenant)
):
    conversation = service.get_conversation(conversation_id)
    if not conversation or str(conversation.tenant_id) != tenant_id:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return conversation

@router.put("/{conversation_id}", response_model=Conversation)
def update_conversation(
    conversation_id: str,
    data: ConversationUpdate,
    tenant_id: str = Depends(get_current_tenant)
):
    # Verify ownership
    conversation = service.get_conversation(conversation_id)
    if not conversation or str(conversation.tenant_id) != tenant_id:
        raise HTTPException(status_code=404, detail="Conversation not found")
    
    if data.status:
        return service.update_status(conversation_id, data.status)
    if data.assigned_agent_id:
        return service.assign_agent(conversation_id, str(data.assigned_agent_id))
    return conversation
