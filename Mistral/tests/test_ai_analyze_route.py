import io
from backend.main import app
from fastapi.testclient import TestClient

client = TestClient(app)

def test_ai_analyze_route(monkeypatch):
    
    fake_result = {
        "skin_type": "Dry",
        "issues": ["Redness"],
        "advice": ["Hydrater"],
        "severity": "Low"
    }

    def fake_chat(**kwargs):
        return {"message": {"content": '{"skin_type": "Dry", "issues": ["Redness"], "advice": ["Hydrater"], "severity": "Low"}'}}

    # Mock ollama
    import backend.services.ai_skin as ai
    monkeypatch.setattr(ai.ollama, "chat", fake_chat)

    files = {"file": ("test.jpg", io.BytesIO(b"fakebytes"), "image/jpeg")}

    response = client.post("/ai-analyze", files=files)

    assert response.status_code == 200
    assert response.json()["skin_type"] == "Dry"
