import io
import json


def login(client):
    return client.post("/login", data={"login": "ensae", "password": "projet20259"})


def test_login_page_ok(client):
    res = client.get("/login")
    assert res.status_code == 200


def test_login_fail(client):
    res = client.post("/login", data={"login": "x", "password": "y"})
    assert res.status_code == 200
    assert b"Identifiants incorrects" in res.data


def test_redirect_if_not_logged(client):
    res = client.get("/upload", follow_redirects=False)
    assert res.status_code in (301, 302)
    assert "/login" in res.headers.get("Location", "")


def test_upload_ok_redirects_processing(client, png_bytes):
    login(client)

    data = {
        "note": "Zone rouge",
        "image": (io.BytesIO(png_bytes), "test.png"),
    }
    res = client.post("/upload", data=data, content_type="multipart/form-data", follow_redirects=False)
    assert res.status_code in (301, 302)
    assert "/processing" in res.headers.get("Location", "")


def test_analyze_ok_after_upload(client, png_bytes):
    login(client)

    data = {
        "note": "Test note",
        "image": (io.BytesIO(png_bytes), "test.png"),
    }
    client.post("/upload", data=data, content_type="multipart/form-data")

    res = client.post("/api/analyze")
    if res.status_code != 200:
        print(res.data.decode("utf-8", errors="ignore"))
    assert res.status_code == 200

    payload = json.loads(res.data)
    assert payload.get("ok") is True


def test_result_contains_metrics(client, png_bytes):
    login(client)

    data = {
        "note": "Test",
        "image": (io.BytesIO(png_bytes), "test.png"),
    }
    client.post("/upload", data=data, content_type="multipart/form-data")
    client.post("/api/analyze")

    res = client.get("/result")
    assert res.status_code == 200
    assert b"URGENCE" in res.data
    assert b"70/100" in res.data

def test_history_page(client):
    login(client)
    res = client.get("/history")
    assert res.status_code == 200

def test_analyze_without_upload(client):
    login(client)
    res = client.post("/api/analyze")
    assert res.status_code == 400
