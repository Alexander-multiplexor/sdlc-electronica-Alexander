from unittest.mock import MagicMock, patch

import pytest

from app.services.reading_service import ReadingService


@pytest.fixture
def mock_repo():
    return MagicMock()

@patch("app.services.reading_service.SensorRepository")
def test_create_reading_service(mock_sensor_repo_class, mock_repo):
    # Simulamos que el repositorio interno del sensor devuelve un sensor válido
    mock_sensor_instance = mock_sensor_repo_class.return_value
    mock_sensor = MagicMock()
    mock_sensor.sensor_type = "temperature"
    mock_sensor.is_active = True
    mock_sensor_instance.get_by_sensor_id.return_value = mock_sensor

    service = ReadingService(reading_repo=mock_repo)
    db = MagicMock()
    
    # Simulamos la lectura entrante
    reading_in = MagicMock()
    reading_in.sensor_id = "S1"
    reading_in.value = 10.0
    reading_in.unit = "C"
    reading_in.sensor_type.value = "temperature"
    
    service.record_reading(db, reading_in)
    mock_repo.create.assert_called_once()