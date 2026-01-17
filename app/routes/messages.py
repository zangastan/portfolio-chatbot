from fastapi import APIRouter, Depends
from typing import List
from app.services.message_service import MessageService
from app.models.message import Message, MessageCreate, MessageResponse
from app.core.dependencies import get_current_tenant

router = APIRouter(prefix="/messages", tags=["messages"])
service = MessageService()

@router.post("/", response_model=MessageResponse)
async def send_message(
    data: MessageCreate,
):
    user_msg, ai_msg = await service.send_message(
        content=data.content
    )
    return MessageResponse(user_message={
        "content": user_msg,
    "role":"user"},
     ai_message=ai_msg)

# @router.get("/{conversation_id}", response_model=List[Message])
# def list_messages(
#     conversation_id: str,
#     tenant_id: str = Depends(get_current_tenant)
# ):
#     # We should verify that conversation belongs to tenant, but for now we list
#     # assuming the client knows the conversation ID. The service could add a check.
#     # Ideally, MessageService should take tenant_id for list filtering too.
#     messages = service.list_messages(conversation_id)
#     # Filter by tenant_id manually if repo doesn't enforce it by join, 
#     # but since messages have tenant_id column:
#     return [m for m in messages if str(m.tenant_id) == tenant_id]
