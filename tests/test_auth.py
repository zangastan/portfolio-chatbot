from unittest.mock import patch

def test_health_check(client_fixture):
    response = client_fixture.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_login_mock(client_fixture):
    # Tests login flow by mocking the auth service call or supabase auth
    with patch("app.services.auth_service.supabase.auth") as mock_auth:
        mock_auth.sign_in_with_password.return_value.session.access_token = "fake-token"
        mock_auth.sign_in_with_password.return_value.user = {"id": "123"}
        
        response = client_fixture.post("/api/v1/auth/login", json={"email": "test@example.com", "password": "pass"})
        assert response.status_code == 200
        assert "access_token" in response.json()
