from app.repositories.base import BaseRepository
from app.models.conversation import Conversation

class ConversationRepository(BaseRepository[Conversation]):
    def __init__(self, client):
        super().__init__(client, "conversations", Conversation)
