from app.repositories.base import BaseRepository
from app.models.ticket import Ticket

class TicketRepository(BaseRepository[Ticket]):
    def __init__(self, client):
        super().__init__(client, "tickets", Ticket)
