from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_home():
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    
    assert "message" in data
    assert data["message"] == "SkinCare Advisor API running"
