from unittest.mock import AsyncMock, MagicMock
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_tilgjengelige_konsulenter(monkeypatch):
    # Lag en imitasjon av respons objekt
    mock_response = MagicMock()
    mock_response.json.return_value = [
        {"id": 1, "navn": "Anna K.", "ferdigheter": ["python"], "belastning_prosent": 40},
        {"id": 2, "navn": "Leo T.", "ferdigheter": ["java"], "belastning_prosent": 80},
    ]
    mock_response.raise_for_status.return_value = None
    
    # Lag en AsyncMock som returnerer imitert respons
    mock_get = AsyncMock(return_value=mock_response)
    
    # Patch httpx.AsyncClient.get metoden
    monkeypatch.setattr("httpx.AsyncClient.get", mock_get)
    
    # Lag API callen
    response = client.get("/tilgjengelige-konsulenter/sammendrag?min_tilgjengelighet_prosent=50&pakrevd_ferdighet=python")
    
    # Asserts sjekker om JSON returnerer gitte nøkkelord
    assert response.status_code == 200
    data = response.json()
    assert "sammendrag" in data
    assert "konsulenter" in data
    
    assert "python" in data["sammendrag"]