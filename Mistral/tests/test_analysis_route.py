# tests/test_analysis_route.py
from fastapi.testclient import TestClient
from unittest.mock import patch
from backend.main import app

client = TestClient(app)


def test_create_analysis_route():
    # Mock de l'analyse Mistral
    with patch("backend.services.skin_analysis.analyze_skin") as mock_ai:
        mock_ai.return_value = {
            "skin_score": 80,
            "type_peau": "mixte",
            "problemes": ["rides"],
            "recommendations": ["hydrater"],
            "raw": "{}"
        }

        files = {
            "file": ("test.jpg", b"fake_image", "image/jpeg")
        }

        # Respecter TA route : /analysis/create/{user_id}
        response = client.post("/analysis/create/1", files=files)
        assert response.status_code == 200


        data = response.json()

        # Vérifications du contenu
        assert data["skin_score"] == 80
        assert data["type_peau"] == "mixte"
