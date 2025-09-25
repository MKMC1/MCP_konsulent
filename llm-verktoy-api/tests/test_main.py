from unittest.mock import AsyncMock, MagicMock
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_tilgjengelige_konsulenter(monkeypatch):
    # Create a mock response object
    mock_response = MagicMock()
    mock_response.json.return_value = [
        {"id": 1, "navn": "Anna K.", "ferdigheter": ["python"], "belastning_prosent": 40},
        {"id": 2, "navn": "Leo T.", "ferdigheter": ["java"], "belastning_prosent": 80},
    ]
    mock_response.raise_for_status.return_value = None
    
    # Create an AsyncMock that returns our mock response
    mock_get = AsyncMock(return_value=mock_response)
    
    # Patch the httpx.AsyncClient.get method
    monkeypatch.setattr("httpx.AsyncClient.get", mock_get)
    
    # Make the API call
    response = client.get("/tilgjengelige-konsulenter/sammendrag?min_tilgjengelighet_prosent=50&pakrevd_ferdighet=python")
    
    # Assertions
    assert response.status_code == 200
    data = response.json()
    assert "sammendrag" in data
    assert "konsulenter" in data
    # Since we're hitting the fallback (OpenRouter will fail in tests), check fallback behavior
    assert "python" in data["sammendrag"]