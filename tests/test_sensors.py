# Tests de integración para CRUD de sensores (200, 201, 204, 404, 409)
from fastapi.testclient import TestClient


def test_health_check(client: TestClient) -> None:
    """Verifica que el endpoint /health responda status ok."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_create_sensor_success(client: TestClient) -> None:
    """Prueba la creación exitosa de un sensor (HTTP 201)."""
    payload = {
        "sensor_id": "TEMP-01",
        "name": "Sensor de Temperatura Principal",
        "sensor_type": "TEMPERATURE",
        "location": "Laboratorio de Electrónica",
    }
    response = client.post("/sensors", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["sensor_id"] == "TEMP-01"
    assert data["is_active"] is True
    assert "id" in data


def test_create_sensor_duplicate_conflict(client: TestClient) -> None:
    """Verifica que intentar crear un sensor duplicate retorne HTTP 409 Conflict."""
    payload = {
        "sensor_id": "TEMP-01",
        "name": "Sensor Original",
        "sensor_type": "TEMPERATURE",
        "location": "Nave A",
    }
    client.post("/sensors", json=payload)

    # Intento de duplicado
    response = client.post("/sensors", json=payload)
    assert response.status_code == 409
    assert "ya existe" in response.json()["detail"]


def test_get_sensor_success_and_not_found(client: TestClient) -> None:
    """Prueba consulta exitosa (200) y caso no encontrado (404)."""
    # 404 Not Found
    response_404 = client.get("/sensors/GHOST-99")
    assert response_404.status_code == 404

    # Crear y consultar (200 OK)
    client.post(
        "/sensors",
        json={
            "sensor_id": "HUM-01",
            "name": "Sensor Humedad",
            "sensor_type": "HUMIDITY",
            "location": "Invernadero",
        },
    )
    response_200 = client.get("/sensors/HUM-01")
    assert response_200.status_code == 200
    assert response_200.json()["sensor_id"] == "HUM-01"


def test_list_sensors_pagination(client: TestClient) -> None:
    """Prueba el listado de sensores con paginación (limit y offset)."""
    for i in range(3):
        client.post(
            "/sensors",
            json={
                "sensor_id": f"SENSOR-0{i}",
                "name": f"Sensor {i}",
                "sensor_type": "PRESSURE",
                "location": "Planta 1",
            },
        )

    response = client.get("/sensors?limit=2&offset=0")
    assert response.status_code == 200
    assert len(response.json()) == 2

    response_offset = client.get("/sensors?limit=2&offset=2")
    assert response_offset.status_code == 200
    assert len(response_offset.json()) == 1


def test_update_and_deactivate_sensor(client: TestClient) -> None:
    """Prueba actualización parcial (PATCH) y borrado lógico (DELETE HTTP 204)."""
    client.post(
        "/sensors",
        json={
            "sensor_id": "TEMP-02",
            "name": "Sensor Vieja Ubicación",
            "sensor_type": "TEMPERATURE",
            "location": "Almacén 1",
        },
    )

    # PATCH
    patch_response = client.patch(
        "/sensors/TEMP-02",
        json={"location": "Almacén 2 Refurbished"},
    )
    assert patch_response.status_code == 200
    assert patch_response.json()["location"] == "Almacén 2 Refurbished"

    # DELETE (Borrado lógico)
    delete_response = client.delete("/sensors/TEMP-02")
    assert delete_response.status_code == 204

    # Verificar inactivo
    get_response = client.get("/sensors/TEMP-02")
    assert get_response.json()["is_active"] is False
