from app.schemas.ticket import TicketCreate, TicketResponse, TicketUpdate
from typing import List
from datetime import datetime

def create_ticket(data: TicketCreate) -> TicketResponse:
    return TicketResponse(
        id="stub_ticket_id",
        title=data.title,
        description=data.description,
        priority=data.priority,
        status="new",
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )

def get_tickets() -> List[TicketResponse]:
    return []

def update_status(id: str, data: TicketUpdate) -> TicketResponse:
    return TicketResponse(
        id=id,
        title="Stub Ticket",
        status=data.status,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
