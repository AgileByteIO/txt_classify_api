from fastapi.testclient import TestClient

from app.app import app

client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"health": "OK"}
