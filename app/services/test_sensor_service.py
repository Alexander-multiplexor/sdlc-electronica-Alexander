import pytest
from unittest.mock import MagicMock
from sqlalchemy.orm import Session

from app.services.sensor_service import SensorService
from app.schemas.sensor import SensorCreate, SensorUpdate
from app.models.sensor_hub import SensorModel
from app.services.exceptions import SensorAlreadyExistsError, SensorNotFoundError

# ==========================================
# FIXTURES (Configuración inicial simulada)
# ==========================================
@pytest.fixture
def mock_repo():
    """Simula el comportamiento del SensorRepository."""
    return MagicMock()

@pytest.fixture
def mock_db():
    """Simula la sesión de la base de datos."""
    return MagicMock(spec=Session)

@pytest.fixture
def sensor_service(mock_repo):
    """Inyecta el repositorio falso en el servicio real."""
    return SensorService(sensor_repo=mock_repo)

# ==========================================
# TESTS PARA CREATE_SENSOR
# ==========================================
def test_create_sensor_success(sensor_service, mock_repo, mock_db):
    # Preparar
    sensor_in = SensorCreate(sensor_id="TEMP_01", type="temperature", unit="C")
    mock_repo.get_by_sensor_id.return_value = None # Simulamos que NO existe
    mock_repo.create.return_value = SensorModel(sensor_id="TEMP_01")
    
    # Ejecutar
    result = sensor_service.create_sensor(mock_db, sensor_in)
    
    # Validar
    assert result.sensor_id == "TEMP_01"
    mock_repo.create.assert_called_once_with(mock_db, sensor_in)

def test_create_sensor_already_exists(sensor_service, mock_repo, mock_db):
    # Preparar
    sensor_in = SensorCreate(sensor_id="TEMP_01", type="temperature", unit="C")
    mock_repo.get_by_sensor_id.return_value = SensorModel(sensor_id="TEMP_01") # Simulamos que SÍ existe
    
    # Ejecutar y Validar Error
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
    mock_repo.get_by_sensor_id.return_value = None # No se encontró
    
    with pytest.raises(SensorNotFoundError):
        sensor_service.get_sensor(mock_db, "UNKNOWN_01")

# ==========================================
# TESTS PARA LIST_SENSORS
# ==========================================
def test_list_sensors(sensor_service, mock_repo, mock_db):
    mock_repo.list_all.return_value = [SensorModel(sensor_id="S1"), SensorModel(sensor_id="S2")]
    
    result = sensor_service.list_sensors(mock_db, limit=10, offset=0)
    assert len(result) == 2
    mock_repo.list_all.assert_called_once_with(mock_db, limit=10, offset=0)

# ==========================================
# TESTS PARA UPDATE_SENSOR
# ==========================================
def test_update_sensor_success(sensor_service, mock_repo, mock_db):
    sensor_update = SensorUpdate(status="maintenance")
    # Para que pase la validación interna de get_sensor
    mock_repo.get_by_sensor_id.return_value = SensorModel(sensor_id="TEMP_01")
    mock_repo.update.return_value = SensorModel(sensor_id="TEMP_01", status="maintenance")
    
    result = sensor_service.update_sensor(mock_db, "TEMP_01", sensor_update)
    assert result.status == "maintenance"
    mock_repo.update.assert_called_once_with(mock_db, "TEMP_01", sensor_update)

# ==========================================
# TESTS PARA DEACTIVATE_SENSOR
# ==========================================
def test_deactivate_sensor_success(sensor_service, mock_repo, mock_db):
    mock_repo.get_by_sensor_id.return_value = SensorModel(sensor_id="TEMP_01")
    mock_repo.deactivate.return_value = SensorModel(sensor_id="TEMP_01", is_active=False)
    
    result = sensor_service.deactivate_sensor(mock_db, "TEMP_01")
    assert result.is_active is False