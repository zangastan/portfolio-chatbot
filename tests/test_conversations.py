from unittest.mock import patch
from app.models.conversation import Conversation
from uuid import UUID

from datetime import datetime

def test_create_conversation(client_fixture):
    # Patch the service instance used in the router
    with patch("app.routes.conversations.service.create_conversation") as mock_create_conv:
        mock_create_conv.return_value = Conversation(
            id=UUID("123e4567-e89b-12d3-a456-426614174000"),
            tenant_id=UUID("123e4567-e89b-12d3-a456-426614174001"),
            visitor_id="vis-1",
            status="open",
            created_at=datetime(2024, 1, 1),
            updated_at=datetime(2024, 1, 1)
        )
        
        response = client_fixture.post(
            "/api/v1/conversations/",
            json={"visitor_id": "vis-1"}
        )
        assert response.status_code == 200, response.text
        data = response.json()
        assert data["visitor_id"] == "vis-1"
        assert data["tenant_id"] == "123e4567-e89b-12d3-a456-426614174001"

def test_list_conversations(client_fixture):
    with patch("app.repositories.base.BaseRepository.list_by_tenant") as mock_list:
        mock_list.return_value = []
        response = client_fixture.get("/api/v1/conversations/")
        assert response.status_code == 200
        assert response.json() == []
