from unittest.mock import MagicMock

import pytest
from sqlalchemy.orm import Session

from app.models.sensor_hub import SensorModel
from app.services.exceptions import SensorAlreadyExistsError, SensorNotFoundError
from app.services.sensor_service import SensorService


# ==========================================
# FIXTURES
# ==========================================
@pytest.fixture
def mock_repo():
    return MagicMock()

@pytest.fixture
def mock_db():
    return MagicMock(spec=Session)

@pytest.fixture
def sensor_service(mock_repo):
    return SensorService(sensor_repo=mock_repo)

# ==========================================
# TESTS PARA CREATE_SENSOR
# ==========================================
def test_create_sensor_success(sensor_service, mock_repo, mock_db):
    sensor_in = MagicMock()
    sensor_in.sensor_id = "TEMP_01"
    
    mock_repo.get_by_sensor_id.return_value = None 
    mock_repo.create.return_value = SensorModel(sensor_id="TEMP_01")
    
    result = sensor_service.create_sensor(mock_db, sensor_in)
    
    assert result.sensor_id == "TEMP_01"
    mock_repo.create.assert_called_once_with(mock_db, sensor_in)

def test_create_sensor_already_exists(sensor_service, mock_repo, mock_db):
    sensor_in = MagicMock()
    sensor_in.sensor_id = "TEMP_01"
    mock_repo.get_by_sensor_id.return_value = SensorModel(sensor_id="TEMP_01") 
    
    with pytest.raises(SensorAlreadyExistsError):
        sensor_service.create_sensor(mock_db, sensor_in)

# ==========================================
# TESTS PARA GET_SENSOR
# ==========================================
def test_get_sensor_success(sensor_service, mock_repo, mock_db):
    mock_repo.get_by_sensor_id.return_value = SensorModel(sensor_id="TEMP_01")
    result = sensor_service.get_sensor(mock_db, "TEMP_01")
    assert result.sensor_id == "TEMP_01"

def test_get_sensor_not_found(sensor_service, mock_repo, mock_db):
    mock_repo.get_by_sensor_id.return_value = None 
    with pytest.raises(SensorNotFoundError):
        sensor_service.get_sensor(mock_db, "UNKNOWN_01")

# ==========================================
# TESTS PARA LIST_SENSORS
# ==========================================
def test_list_sensors(sensor_service, mock_repo, mock_db):
    mock_repo.list_all.return_value = [SensorModel(sensor_id="S1"), SensorModel(sensor_id="S2")]
    result = sensor_service.list_sensors(mock_db, limit=10, offset=0)
    assert len(result) == 2

# ==========================================
# TESTS PARA UPDATE_SENSOR
# ==========================================
def test_update_sensor_success(sensor_service, mock_repo, mock_db):
    sensor_update = MagicMock()
    mock_repo.get_by_sensor_id.return_value = SensorModel(sensor_id="TEMP_01")
    mock_repo.update.return_value = SensorModel(sensor_id="TEMP_01", location="Nueva")
    
    result = sensor_service.update_sensor(mock_db, "TEMP_01", sensor_update)
    assert result.location == "Nueva"

# ==========================================
# TESTS PARA DEACTIVATE_SENSOR
# ==========================================
def test_deactivate_sensor_success(sensor_service, mock_repo, mock_db):
    mock_repo.get_by_sensor_id.return_value = SensorModel(sensor_id="TEMP_01")
    mock_repo.deactivate.return_value = SensorModel(sensor_id="TEMP_01", is_active=False)
    
    result = sensor_service.deactivate_sensor(mock_db, "TEMP_01")
    assert result.is_active is False