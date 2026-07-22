import pytest

from semana2.eval1.src.sensor_reading import SensorReading


def test_sensor_reading_creacion_valida():
    reading = SensorReading(sensor_id="TEMP-01", temperature=25.0, humidity=50.0)
    assert reading.sensor_id == "TEMP-01"
    assert reading.temperature == 25.0
    assert reading.humidity == 50.0

def test_sensor_reading_temperatura_invalida_lanza_error():
    with pytest.raises(ValueError, match="Temperatura fuera de rango"):
        SensorReading(sensor_id="TEMP-01", temperature=120.0, humidity=50.0)

def test_sensor_reading_humedad_invalida_lanza_error():
    with pytest.raises(ValueError, match="Humedad fuera de rango"):
        SensorReading(sensor_id="TEMP-01", temperature=20.0, humidity=-5.0)