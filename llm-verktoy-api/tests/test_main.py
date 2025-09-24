from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

# Vi monkeypatcher httpx-kallet
def fake_get(*args, **kwargs):
    class FakeResponse:
        def json(self):
            return [
                {"id": 1, "navn": "Anna K.", "ferdigheter": ["python"], "belastning_prosent": 40},
                {"id": 2, "navn": "Leo T.", "ferdigheter": ["java"], "belastning_prosent": 80},
            ]
    return FakeResponse()

def test_tilgjengelige_konsulenter(monkeypatch):
    monkeypatch.setattr("httpx.AsyncClient.get", lambda *a, **k: fake_get())
    
    response = client.get("/tilgjengelige-konsulenter/sammendrag?min_tilgjengelighet_prosent=50&påkrevd_ferdighet=python")
    assert response.status_code == 200
    data = response.json()
    assert "sammendrag" in data
    assert "Anna K." in data["sammendrag"]
