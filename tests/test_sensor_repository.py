from unittest.mock import MagicMock

import pytest
from sqlalchemy.orm import Session

from app.models.sensor_hub import SensorModel
from app.repositories.sensor_repository import SensorRepository
from app.schemas.sensor import SensorUpdate


# ==========================================
# FIXTURES
# ==========================================
@pytest.fixture
def mock_db():
    """Simula la sesión de SQLAlchemy."""
    return MagicMock(spec=Session)


@pytest.fixture
def repository():
    """Instancia limpia del repositorio para cada test."""
    return SensorRepository()


# ==========================================
# TESTS PARA CREATE
# ==========================================
def test_create_sensor(repository, mock_db):
    # Simulamos el objeto de entrada (SensorCreate)
    sensor_in_mock = MagicMock()
    sensor_in_mock.sensor_id = "TEMP-01"
    sensor_in_mock.name = "Termómetro"
    sensor_in_mock.sensor_type.value = "temperature"
    sensor_in_mock.location = "Planta 1"

    # Ejecutamos
    result = repository.create(mock_db, sensor_in_mock)

    # Validamos
    assert result.sensor_id == "TEMP-01"
    assert result.is_active is True
    assert result.name == "Termómetro"

    # Validamos que se llamó a la base de datos correctamente
    mock_db.add.assert_called_once()
    mock_db.commit.assert_called_once()
    mock_db.refresh.assert_called_once()


# ==========================================
# TESTS PARA GET_BY_SENSOR_ID
# ==========================================
def test_get_by_sensor_id(repository, mock_db):
    # Simulamos que la DB encuentra el registro
    mock_db.scalar.return_value = SensorModel(sensor_id="TEMP-01")

    result = repository.get_by_sensor_id(mock_db, "TEMP-01")

    assert result.sensor_id == "TEMP-01"
    mock_db.scalar.assert_called_once()


# ==========================================
# TESTS PARA LIST_ALL
# ==========================================
def test_list_all(repository, mock_db):
    # Simulamos el encadenamiento de db.scalars().all()
    mock_scalars = MagicMock()
    mock_scalars.all.return_value = [SensorModel(sensor_id="S1"), SensorModel(sensor_id="S2")]
    mock_db.scalars.return_value = mock_scalars

    result = repository.list_all(mock_db, limit=10, offset=0)

    assert len(result) == 2
    mock_db.scalars.assert_called_once()
    mock_scalars.all.assert_called_once()


# ==========================================
# TESTS PARA UPDATE
# ==========================================
def test_update_success(repository, mock_db):
    # Forzamos get_by_sensor_id para que devuelva un sensor existente
    mock_sensor = SensorModel(sensor_id="TEMP-01", location="Vieja")
    repository.get_by_sensor_id = MagicMock(return_value=mock_sensor)

    # Simulamos los datos de actualización
    update_data_mock = MagicMock(spec=SensorUpdate)
    update_data_mock.model_dump.return_value = {"location": "Nueva"}

    result = repository.update(mock_db, "TEMP-01", update_data_mock)

    assert result.location == "Nueva"
    mock_db.commit.assert_called_once()
    mock_db.refresh.assert_called_once_with(mock_sensor)


def test_update_not_found(repository, mock_db):
    # Si no existe, devuelve None y no hace commit
    repository.get_by_sensor_id = MagicMock(return_value=None)

    result = repository.update(mock_db, "INEXISTENTE", MagicMock())

    assert result is None
    mock_db.commit.assert_not_called()


# ==========================================
# TESTS PARA DEACTIVATE
# ==========================================
def test_deactivate_success(repository, mock_db):
    mock_sensor = SensorModel(sensor_id="TEMP-01", is_active=True)
    repository.get_by_sensor_id = MagicMock(return_value=mock_sensor)

    result = repository.deactivate(mock_db, "TEMP-01")

    assert result.is_active is False
    mock_db.commit.assert_called_once()
    mock_db.refresh.assert_called_once_with(mock_sensor)


def test_deactivate_not_found(repository, mock_db):
    repository.get_by_sensor_id = MagicMock(return_value=None)

    result = repository.deactivate(mock_db, "INEXISTENTE")

    assert result is None
    mock_db.commit.assert_not_called()
