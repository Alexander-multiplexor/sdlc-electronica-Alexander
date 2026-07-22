from semana2.eval1.src.sensor_reading import SensorReading
from semana2.eval1.src.anomaly_detector import AnomalyDetector

def test_detector_temperatura_alta():
    detector = AnomalyDetector(max_temp=35.0, max_humidity=80.0)
    reading = SensorReading(sensor_id="TEMP-01", temperature=36.5, humidity=50.0)
    is_anomaly, reason = detector.evaluate(reading)
    assert is_anomaly is True
    assert "TEMPERATURA_ALTA" in reason

def test_detector_humedad_alta():
    detector = AnomalyDetector(max_temp=35.0, max_humidity=80.0)
    reading = SensorReading(sensor_id="TEMP-01", temperature=22.0, humidity=85.0)
    is_anomaly, reason = detector.evaluate(reading)
    assert is_anomaly is True
    assert "HUMEDAD_ALTA" in reason

def test_detector_lectura_normal():
    detector = AnomalyDetector(max_temp=35.0, max_humidity=80.0)
    reading = SensorReading(sensor_id="TEMP-01", temperature=24.0, humidity=45.0)
    is_anomaly, reason = detector.evaluate(reading)
    assert is_anomaly is False
    assert reason == "NORMAL"