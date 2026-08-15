from fastapi.testclient import TestClient


def test_create_reading_success(client: TestClient) -> None:
    """Prueba ingesta correcta de una lectura dentro del rango físico (HTTP 201)."""
    # Crear sensor previo
    client.post(
        "/sensors",
        json={
            "sensor_id": "TEMP-01",
            "name": "Sensor Térmico",
            "sensor_type": "TEMPERATURE",
            "location": "Cuarto de Máquinas",
        },
    )

    payload = {
        "sensor_id": "TEMP-01",
        "value": 25.5,
        "unit": "C",
        "sensor_type": "TEMPERATURE",
    }
    response = client.post("/sensors/TEMP-01/readings", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["value"] == 25.5
    assert data["unit"] == "C"


def test_create_reading_physics_out_of_range(client: TestClient) -> None:
    """Verifica que rechace lecturas fuera del rango físico (HTTP 422)."""
    client.post(
        "/sensors",
        json={
            "sensor_id": "TEMP-01",
            "name": "Sensor Térmico",
            "sensor_type": "TEMPERATURE",
            "location": "Lab",
        },
    )

    # 500 °C está fuera del rango [-50, 150]
    payload = {
        "sensor_id": "TEMP-01",
        "value": 500.0,
        "unit": "C",
        "sensor_type": "TEMPERATURE",
    }
    response = client.post("/sensors/TEMP-01/readings", json=payload)
    assert response.status_code == 422


def test_create_reading_invalid_unit(client: TestClient) -> None:
    """Verifica que rechace unidades desconocidas para el tipo de sensor (HTTP 422)."""
    client.post(
        "/sensors",
        json={
            "sensor_id": "HUM-01",
            "name": "Humedad",
            "sensor_type": "HUMIDITY",
            "location": "Invernadero",
        },
    )

    # "Km/h" no es unidad válida para HUMIDITY
    payload = {
        "sensor_id": "HUM-01",
        "value": 50.0,
        "unit": "Km/h",
        "sensor_type": "HUMIDITY",
    }
    response = client.post("/sensors/HUM-01/readings", json=payload)
    assert response.status_code == 422


def test_create_reading_sensor_not_found(client: TestClient) -> None:
    """Verifica HTTP 404 al enviar lectura a un sensor no registrado."""
    payload = {
        "sensor_id": "GHOST-99",
        "value": 20.0,
        "unit": "C",
        "sensor_type": "TEMPERATURE",
    }
    response = client.post("/sensors/GHOST-99/readings", json=payload)
    assert response.status_code == 404


def test_create_reading_inactive_sensor(client: TestClient) -> None:
    """Verifica HTTP 400 al intentar registrar lectura en sensor inactivo."""
    client.post(
        "/sensors",
        json={
            "sensor_id": "TEMP-OFF",
            "name": "Sensor Inactivo",
            "sensor_type": "TEMPERATURE",
            "location": "Sótano",
        },
    )
    # Desactivar
    client.delete("/sensors/TEMP-OFF")

    payload = {
        "sensor_id": "TEMP-OFF",
        "value": 22.0,
        "unit": "C",
        "sensor_type": "TEMPERATURE",
    }
    response = client.post("/sensors/TEMP-OFF/readings", json=payload)
    assert response.status_code == 400
    assert "se encuentra inactivo" in response.json()["detail"]


def test_create_reading_type_mismatch(client: TestClient) -> None:
    """Verifica HTTP 400 al enviar lectura de tipo incoherente con el sensor."""
    client.post(
        "/sensors",
        json={
            "sensor_id": "TEMP-01",
            "name": "Sensor Temperatura",
            "sensor_type": "TEMPERATURE",
            "location": "Nave B",
        },
    )

    # Intentar mandar lectura de HUMIDITY a un sensor de TEMPERATURE
    payload = {
        "sensor_id": "TEMP-01",
        "value": 60.0,
        "unit": "%",
        "sensor_type": "HUMIDITY",
    }
    response = client.post("/sensors/TEMP-01/readings", json=payload)
    assert response.status_code == 400
    assert "incompatible" in response.json()["detail"]


def test_list_readings_with_filters(client: TestClient) -> None:
    """Prueba consulta de lecturas por sensor con paginación y filtros de fecha."""
    client.post(
        "/sensors",
        json={
            "sensor_id": "PRES-01",
            "name": "Presión Barométrica",
            "sensor_type": "PRESSURE",
            "location": "Torre Control",
        },
    )

    for val in [1013.2, 1014.0, 1015.5]:
        client.post(
            "/sensors/PRES-01/readings",
            json={
                "sensor_id": "PRES-01",
                "value": val,
                "unit": "hPa",
                "sensor_type": "PRESSURE",
            },
        )

    response = client.get("/sensors/PRES-01/readings?limit=2&offset=0")
    assert response.status_code == 200
    assert len(response.json()) == 2
