from unittest.mock import patch
from fastapi.testclient import TestClient

from app.main import app
from app.db.schema import User
from app.services.auth_services import password_hash

client = TestClient(app)

def test_login_success():
    test_password = "mysecretpassword"
    hashed_pwd = password_hash.hash(test_password)
    
    fake_user = User(
        user_id=1,
        username="testuser",
        name="Test User",
        email="test@example.com",
        password=hashed_pwd,
        alert=True
    )

    with patch("app.services.auth_services.get_user_by_username") as mock_db_call:
        mock_db_call.return_value = fake_user

        response = client.post(
            "/auth/login",
            data={"username": "testuser", "password": test_password}
        )

    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_login_wrong_password():
    fake_user = User(
        user_id=1,
        username="testuser",
        password=password_hash.hash("realpassword"),
        name="Test",
        email="t@t.com"
    )

    with patch("app.services.auth_services.get_user_by_username") as mock_db_call:
        mock_db_call.return_value = fake_user
        
        response = client.post(
            "/auth/login",
            data={"username": "testuser", "password": "wrongpassword"}
        )

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid credentials"