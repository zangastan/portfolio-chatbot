from datetime import datetime
from typing import List
from app.repositories.ticket_repo import TicketRepository
from app.models.ticket import Ticket
from app.core.database import supabase

class TicketService:
    def __init__(self):
        self.repo = TicketRepository(supabase)

    def create_ticket(self, tenant_id: str, conversation_id: str, priority: str, description: str) -> Ticket:
        return self.repo.create({
            "tenant_id": tenant_id,
            "conversation_id": conversation_id,
            "status": "open",
            "priority": priority,
            "description": description,
            "created_at": datetime.utcnow().isoformat()
        })

    def list_tickets(self, tenant_id: str) -> List[Ticket]:
        return self.repo.list_by_tenant(tenant_id)
    
    def update_status(self, ticket_id: str, status: str) -> Ticket:
        return self.repo.update(ticket_id, {"status": status})
