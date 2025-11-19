# tests/test_user_routes.py
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_create_and_get_user_route():
    payload = {
        "age": 28,
        "sexe": "F",
        "type_peau_habituel": "mixte"
    }

    # 1) Création utilisateur
    rresp = client.post("/user/create", json=payload)
    assert resp.status_code == 200

    data = resp.json()
    assert "id" in data
    assert data["id"] is not None

    user_id = data["id"]

    # 2) Récupération utilisateur
    resp2 = client.get(f"/user/get/1{user_id}")
    assert resp2.status_code == 200
    assert resp2.json()["id"] == user_id
