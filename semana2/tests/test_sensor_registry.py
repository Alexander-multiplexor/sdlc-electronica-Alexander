import pytest
from src.sensor_registry import SensorRegistry, SensorNotFoundError


def test_get_unknown_sensor_raises():
    registry = SensorRegistry()
    with pytest.raises(SensorNotFoundError):
        registry.get("GHOST-99")


def test_register_and_get_sensor_success():
    registry = SensorRegistry()
    registry.register("TEMP-01", "Temperatura", "Nave A")
    sensor = registry.get("TEMP-01")

    assert sensor["id"] == "TEMP-01"
    assert sensor["type"] == "Temperatura"
    assert sensor["status"] == "ACTIVO"