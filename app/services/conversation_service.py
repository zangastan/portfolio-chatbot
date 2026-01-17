from typing import List, Optional
from datetime import datetime
from app.repositories.conversation_repo import ConversationRepository
from app.models.conversation import Conversation
from app.core.database import supabase

class ConversationService:
    def __init__(self):
        self.repo = ConversationRepository(supabase)

    def create_conversation(self, tenant_id: str, visitor_id: str) -> Conversation:
        # Check if active conversation exists for this visitor? 
        # For simplicity, always create new for now or return existing open one.
        return self.repo.create({
            "tenant_id": tenant_id,
            "visitor_id": visitor_id,
            "status": "open",
            "created_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat()
        })

    def get_conversation(self, conversation_id: str) -> Optional[Conversation]:
        return self.repo.get_by_id(conversation_id)

    def list_conversations(self, tenant_id: str) -> List[Conversation]:
        return self.repo.list_by_tenant(tenant_id)

    def update_status(self, conversation_id: str, status: str) -> Conversation:
        return self.repo.update(conversation_id, {
            "status": status, 
            "updated_at": datetime.utcnow().isoformat()
        })

    def assign_agent(self, conversation_id: str, agent_id: str) -> Conversation:
        return self.repo.update(conversation_id, {
            "assigned_agent_id": agent_id,
            "updated_at": datetime.utcnow().isoformat()
        })
