from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)
# Tester at dataen inneholder parametere spesifisert i case
def test_get_konsulenter():
    response = client.get("/konsulenter")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert "id" in data[0]
    assert "navn" in data[0]
    assert "ferdigheter" in data[0]
    assert "belastning_prosent" in data[0]
