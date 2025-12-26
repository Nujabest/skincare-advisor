import pytest
from flask.testing import FlaskClient
import app


def small_png() -> bytes:
    return (
        b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR"
        b"\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00"
        b"\x1f\x15\xc4\x89\x00\x00\x00\x0cIDATx\x9cc\xf8\xff\xff?\x00\x05\xfe\x02\xfe"
        b"\xa7\x9e\x1d\xdd\x00\x00\x00\x00IEND\xaeB`\x82"
    )


@pytest.fixture
def client(monkeypatch) -> FlaskClient:
    monkeypatch.setenv("DEMO_LOGIN", "ensae")
    monkeypatch.setenv("DEMO_PASSWORD", "projet20259")
    monkeypatch.setenv("MISTRAL_API_KEY", "fake-key")

    # IMPORTANT: same signature as in app.py
    def fake_ai(data_uri: str, user_text: str) -> str:
        return (
            'METRICS: {"urgence":"faible","score_peau":70,"confiance":"moyenne",'
            '"inflammation":"faible","acne":"légère","risque_irritation":"moyen"}\n'
            "DIAGNOSTIC PROBABLE (avec prudence)\n"
            "Diagnostic de test.\n"
        )

    monkeypatch.setattr(app, "mistral_vision_chat", fake_ai)

    app.app.config["TESTING"] = True
    return app.app.test_client()


@pytest.fixture
def png_bytes() -> bytes:
    return small_png()

