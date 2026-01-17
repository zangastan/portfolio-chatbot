from app.repositories.base import BaseRepository
from app.models.knowledge import KnowledgeDocument

class KnowledgeRepository(BaseRepository[KnowledgeDocument]):
    def __init__(self, client):
        super().__init__(client, "knowledge", KnowledgeDocument)
