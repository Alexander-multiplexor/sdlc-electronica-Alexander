from pathlib import Path

from semana2.eval1.src.alert_manager import (
    AlertManager,
    ConsoleAlertStrategy,
    FileAlertStrategy,
)
from semana2.eval1.src.anomaly_detector import AnomalyDetector
from semana2.eval1.src.sensor_simulator import SensorSimulator


def test_integration_10_sensors_60_cycles(tmp_path: Path) -> None:
    """Test de integración: 10 sensores x 60 ciclos = 600 lecturas procesadas."""
    log_file = tmp_path / "integration_alerts.log"

    # 1. Instanciar componentes del sistema
    simulator = SensorSimulator(num_sensors=10)
    detector = AnomalyDetector(max_temp=35.0, max_humidity=80.0)

    alert_manager = AlertManager()
    alert_manager.add_strategy(ConsoleAlertStrategy())
    alert_manager.add_strategy(FileAlertStrategy(log_file))

    total_readings = 0
    anomalies_count = 0

    # 2. Ejecutar 60 ciclos de monitoreo
    for cycle in range(60):
        cycle_readings = simulator.generate_cycle()
        assert len(cycle_readings) == 10

        for reading in cycle_readings:
            total_readings += 1
            is_anomaly, reason = detector.evaluate(reading)

            if is_anomaly:
                anomalies_count += 1
                alert_manager.notify(f"Ciclo {cycle + 1:02d} | {reading.sensor_id}: {reason}")

    # 3. Verificaciones de integración
    assert total_readings == 600
    assert log_file.exists()

    if anomalies_count > 0:
        log_content = log_file.read_text(encoding="utf-8")
        assert "Ciclo" in log_content
