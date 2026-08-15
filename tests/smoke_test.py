from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_smoke() -> None:
    """Verifica que el servicio responda correctamente en su endpoint de salud."""
    response = client.get("/health")
    assert response.status_code == 200