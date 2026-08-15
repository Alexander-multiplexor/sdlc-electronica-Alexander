import pytest

from semana1.solid_srp_ocp_lsp import (
    AnomalyDetector,
    ConsoleAlert,
    DataLogger,
    HumiditySensor,
    SensorReader,
    SensorReading,
    TemperatureSensor,
    process_sensor,
)


# =====================================================================
# TESTS: SRP
# =====================================================================
def test_srp_reader_returns_correct_reading():
    reader = SensorReader()
    reading = reader.read_hardware()
    assert isinstance(reading, SensorReading)
    assert reading.sensor_id == "TEMP-01"


def test_srp_logger_executes_without_errors():
    logger = DataLogger()
    reading = SensorReading("TEMP-01", 24.5)
    # Validamos que la responsabilidad de guardado se ejecute limpiamente
    try:
        logger.save(reading)
    except Exception as e:
        pytest.fail(f"DataLogger levantó una excepción inesperada: {e}")


# =====================================================================
# TESTS: OCP
# =====================================================================
class MockAlert(ConsoleAlert):
    """Clase espía para validar que la estrategia fue llamada sin modificar el detector."""

    def __init__(self):
        self.message_sent = None

    def send(self, message: str) -> None:
        self.message_sent = message


def test_ocp_triggers_alert_when_threshold_exceeded():
    mock_alert = MockAlert()
    detector = AnomalyDetector(alert=mock_alert, threshold=30.0)

    # Lectura que supera el límite de 30.0
    detector.check(SensorReading("TEMP-MAX", 35.0))
    assert mock_alert.message_sent == "Anomalía en TEMP-MAX"


def test_ocp_does_not_trigger_alert_under_threshold():
    mock_alert = MockAlert()
    detector = AnomalyDetector(alert=mock_alert, threshold=30.0)

    # Lectura segura
    detector.check(SensorReading("TEMP-MIN", 20.0))
    assert mock_alert.message_sent is None


# =====================================================================
# TESTS: LSP
# =====================================================================
def test_lsp_temperature_sensor_substitution():
    temp_sensor = TemperatureSensor()
    # Debe comportarse de forma idéntica bajo la abstracción BaseSensor
    assert process_sensor(temp_sensor) == 25.3


def test_lsp_humidity_sensor_substitution():
    hyd_sensor = HumiditySensor()
    # Intercambiable sin alterar la ejecución del cliente
    assert process_sensor(hyd_sensor) == 60.1
