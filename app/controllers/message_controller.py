from app.schemas.message import MessageCreate, MessageResponse
from typing import List
from datetime import datetime
from app.services.automation_service import AutomationService
import asyncio

automation_service = AutomationService()

async def send_message(tenant_id: str, data: MessageCreate) -> MessageResponse:
    # 1. Save User Message (Stub functionality maintained, but in real app saves to DB)
    user_msg_response = MessageResponse(
        id="stub_msg_id",
        content=data.content,
        sender_type=data.sender_type,
        timestamp=datetime.utcnow()
    )
    
    # 2. Trigger AI if user message
    if data.sender_type == "user":
        # In a real async system, this might be a background task or immediate
        ai_result = await automation_service.generate_response(tenant_id, data.content)
        
        # We might return the AI response here or assume the frontend polls/sockets receive it.
        # For this stub/MVC, let's just print it or return it if the schema allowed list of messages.
        # But the signature returns single MessageResponse.
        print(f"AI Response: {ai_result}")
        
    return user_msg_response

def get_messages(conversation_id: str) -> List[MessageResponse]:
    return [
        MessageResponse(
            id="stub_msg_1",
            content="Hello",
            sender_type="user",
            timestamp=datetime.utcnow()
        )
    ]
