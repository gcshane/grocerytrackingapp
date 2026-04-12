from fastapi.testclient import TestClient
from unittest.mock import patch

from app.main import app

client = TestClient(app)

def test_startup_calls_init_db():
    with patch("app.main.init_db") as mock_init_db:
        with TestClient(app):
            pass  
        mock_init_db.assert_called_once()

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}