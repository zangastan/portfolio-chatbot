from typing import List
from app.repositories.base import BaseRepository
from app.models.message import Message

class MessageRepository(BaseRepository[Message]):
    def __init__(self, client):
        super().__init__(client, "messages", Message)
    
    # def get_by_conversation(self, conversation_id: str) -> List[Message]:
    #     response = self.client.table(self.table)\
    #         .select("*")\
    #         .eq("conversation_id", conversation_id)\
    #         .order("created_at")\
    #         .execute()
    #     return [self.model(**item) for item in response.data]
