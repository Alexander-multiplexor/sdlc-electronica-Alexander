from datetime import datetime, timezone

import pytest

from app.domain.exceptions import RepositoryError
from app.models.reading import ReadingModel
from app.services.sensor_service import ReadingRepositoryInterface, SensorService


class FakeReadingRepository(ReadingRepositoryInterface):
    """Repositorio en memoria para tests unitarios rápidos y deterministas."""

    def __init__(self, should_fail: bool = False) -> None:
        self.readings: list[ReadingModel] = []
        self.should_fail = should_fail

    async def save(self, reading: ReadingModel) -> ReadingModel:
        if self.should_fail:
            raise ConnectionError("DB Connection Timeout")
        reading.id = len(self.readings) + 1
        reading.timestamp = datetime.now(timezone.utc)
        self.readings.append(reading)
        return reading

    async def get_latest(self, sensor_id: str) -> ReadingModel | None:
        matches = [r for r in self.readings if r.sensor_id == sensor_id]
        return matches[-1] if matches else None


# Test 1: Flujo exitoso de registro
@pytest.mark.anyio
async def test_register_reading_success() -> None:
    repo = FakeReadingRepository()
    service = SensorService(repository=repo)

    result = await service.register_reading(sensor_id="TEMP_MODBUS_01", value=24.5)

    assert result.id == 1
    assert result.sensor_id == "TEMP_MODBUS_01"
    assert result.value == 24.5


# Test 2: Validación de sensor_id vacío o con solo espacios en blanco
@pytest.mark.anyio
async def test_register_reading_empty_sensor_id_raises_value_error() -> None:
    repo = FakeReadingRepository()
    service = SensorService(repository=repo)

    with pytest.raises(ValueError, match="sensor_id no puede estar vacío"):
        await service.register_reading(sensor_id="   ", value=10.0)


# Test 3: Encapsulación de errores de infraestructura a dominio (RepositoryError)
@pytest.mark.anyio
async def test_register_reading_encapsulates_repository_exception() -> None:
    repo = FakeReadingRepository(should_fail=True)
    service = SensorService(repository=repo)

    with pytest.raises(RepositoryError, match="Error en la capa de persistencia"):
        await service.register_reading(sensor_id="ADC_CH0", value=3.29)


# Test 4: Manejo de valores extremos de punto flotante y negativos
@pytest.mark.anyio
async def test_register_reading_negative_and_extreme_floating_point() -> None:
    repo = FakeReadingRepository()
    service = SensorService(repository=repo)

    result = await service.register_reading(sensor_id="TEMP_CRYO", value=-271.15)
    assert result.value == -271.15


# Test 5: Aislamiento entre múltiples sensores y obtención de última lectura
@pytest.mark.anyio
async def test_reading_isolation_multiple_sensors() -> None:
    repo = FakeReadingRepository()
    service = SensorService(repository=repo)

    await service.register_reading(sensor_id="SENSOR_A", value=10.0)
    await service.register_reading(sensor_id="SENSOR_B", value=20.0)
    await service.register_reading(sensor_id="SENSOR_A", value=15.5)

    latest_a = await repo.get_latest("SENSOR_A")
    latest_b = await repo.get_latest("SENSOR_B")

    assert latest_a is not None and latest_a.value == 15.5
    assert latest_b is not None and latest_b.value == 20.0
