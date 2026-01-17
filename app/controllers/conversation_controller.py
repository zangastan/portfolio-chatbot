from app.schemas.conversation import ConversationCreate, ConversationResponse, ConversationUpdate, AssignAgentRequest
from datetime import datetime

def start_conversation(data: ConversationCreate) -> ConversationResponse:
    return ConversationResponse(
        id="stub_conv_id",
        subject=data.subject,
        status="open",
        created_at=datetime.utcnow()
    )

def get_conversation(id: str) -> ConversationResponse:
    return ConversationResponse(
        id=id,
        subject="Stub Subject",
        status="open",
        created_at=datetime.utcnow()
    )

def assign_agent(id: str, data: AssignAgentRequest) -> ConversationResponse:
    return ConversationResponse(
        id=id,
        subject="Stub Subject",
        status="assigned",
        assigned_agent_id=data.agent_id,
        created_at=datetime.utcnow()
    )

def close_conversation(id: str) -> ConversationResponse:
    return ConversationResponse(
        id=id,
        subject="Stub Subject",
        status="closed",
        created_at=datetime.utcnow()
    )
