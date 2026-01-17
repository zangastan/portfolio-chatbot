from fastapi import APIRouter, Depends
from typing import List
from app.services.ticket_service import TicketService
from app.models.ticket import Ticket, TicketCreate, TicketUpdate
from app.core.dependencies import get_current_tenant

router = APIRouter(prefix="/tickets", tags=["tickets"])
service = TicketService()

@router.post("/", response_model=Ticket)
def create_ticket(
    data: TicketCreate, 
    tenant_id: str = Depends(get_current_tenant)
):
    return service.create_ticket(
        tenant_id, 
        str(data.conversation_id), 
        data.priority, 
        data.description
    )

@router.get("/", response_model=List[Ticket])
def list_tickets(tenant_id: str = Depends(get_current_tenant)):
    return service.list_tickets(tenant_id)

@router.patch("/{ticket_id}", response_model=Ticket)
def update_ticket(
    ticket_id: str, 
    data: TicketUpdate, 
    tenant_id: str = Depends(get_current_tenant)
):
    # Add ownership check here in real app
    if data.status:
        return service.update_status(ticket_id, data.status)
    return service.repo.get_by_id(ticket_id)
