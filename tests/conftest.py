import pytest
from unittest.mock import MagicMock
from fastapi.testclient import TestClient
from app.main import app
from app.core.database import supabase
from app.core.dependencies import get_current_user

@pytest.fixture
def mock_supabase():
    # Mock the supabase client to prevent network calls
    client = MagicMock()
    # Mock table chaining: client.table(name).select(..).eq(..).execute()
    client.table.return_value.select.return_value.eq.return_value.execute.return_value.data = []
    client.table.return_value.insert.return_value.execute.return_value.data = [{}]
    client.table.return_value.update.return_value.eq.return_value.execute.return_value.data = [{}]
    return client

@pytest.fixture
def client_fixture(mock_supabase):
    # Override the supabase client in the app if feasible, or just rely on patching in tests
    # Since supabase is a module level var, we might need to patch it in the modules under test
    # But for integration tests using TestClient, dependecy overrides are cleaner for Auth
    
    app.dependency_overrides[get_current_user] = lambda: {
        "sub": "123e4567-e89b-12d3-a456-426614174000", 
        "app_metadata": {"tenant_id": "123e4567-e89b-12d3-a456-426614174001"}
    }
    
    with TestClient(app) as client:
        yield client
    
    app.dependency_overrides.clear()
