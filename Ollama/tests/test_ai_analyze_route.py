import io
from backend.main import app
from fastapi.testclient import TestClient

client = TestClient(app)

def test_ai_analyze_route(monkeypatch):

    def fake_chat(**kwargs):
        return {
            "message": {
                "content": '{"skin_type": "Dry", "issues": ["Redness"], "advice": ["Hydrater"], "severity": "Low"}'
            }
        }

    # Mock ollama / mistral selon ton service
    import backend.services.ai_skin as ai
    monkeypatch.setattr(ai, "ollama", type("obj", (), {"chat": fake_chat}))

    files = {"file": ("test.jpg", io.BytesIO(b"fakebytes"), "image/jpeg")}
    response = client.post("/ai-analyze", files=files)

    assert response.status_code == 200
    assert response.json()["skin_type"] == "Dry"
