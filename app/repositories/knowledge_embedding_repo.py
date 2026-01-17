from typing import List, Dict, Any
from app.repositories.base import BaseRepository
from app.models.knowledge_embedding import KnowledgeEmbedding

class KnowledgeEmbeddingRepository(BaseRepository[KnowledgeEmbedding]):
    def __init__(self, client):
        super().__init__(client, "knowledge_embeddings", KnowledgeEmbedding)

    def create_batch(self, embeddings: List[Dict[str, Any]]) -> List[KnowledgeEmbedding]:
        response = self.client.table(self.table).insert(embeddings).execute()
        return [self.model(**item) for item in response.data]

    def search_similar(self, embedding: List[float], tenant_id: str, match_threshold: float = 0.5, match_count: int = 5):
        """
        Uses Supabase RPC 'match_documents' for similarity search.
        Includes tenant_id for isolation.
        """
        params = {
            "p_tenant_id": tenant_id,
            "query_embedding": embedding,
            "match_threshold": match_threshold,
            "match_count": match_count
        }
        response = self.client.rpc("match_documents", params).execute()
        
        return [self.model(**item) for item in response.data]
