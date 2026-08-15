"""Suite de pruebas unitarias TDD para la feature de detección de anomalías."""

import pytest

from app.features.anomalies import (
    AnomalyDetectionService,
    LogAlertStrategy,
    SensorThresholdConfig,
    WebhookAlertStrategy,
)


@pytest.mark.anyio
async def test_no_anomaly_when_within_normal_range() -> None:
    """Verifica que lecturas dentro de los límites no disparen eventos ni alertas."""
    log_strat = LogAlertStrategy()
    service = AnomalyDetectionService(strategies=[log_strat])
    config = SensorThresholdConfig(sensor_id="TEMP-01", min_value=10.0, max_value=40.0)

    event = await service.evaluate_reading(sensor_id="TEMP-01", value=25.0, config=config)

    assert event is None
    assert len(service.get_anomalies()) == 0
    assert len(log_strat.sent_alerts) == 0


@pytest.mark.anyio
async def test_detects_upper_threshold_anomaly() -> None:
    """Verifica detección de anomalía por superación de límite superior."""
    log_strat = LogAlertStrategy()
    service = AnomalyDetectionService(strategies=[log_strat])
    config = SensorThresholdConfig(sensor_id="TEMP-01", min_value=10.0, max_value=50.0)

    event = await service.evaluate_reading(sensor_id="TEMP-01", value=58.5, config=config)

    assert event is not None
    assert event.sensor_id == "TEMP-01"
    assert event.rule == "MAX_EXCEEDED"
    assert event.value == 58.5
    assert event.limit == 50.0
    assert len(log_strat.sent_alerts) == 1


@pytest.mark.anyio
async def test_detects_lower_threshold_anomaly() -> None:
    """Verifica detección de anomalía por estar por debajo del límite inferior."""
    log_strat = LogAlertStrategy()
    service = AnomalyDetectionService(strategies=[log_strat])
    config = SensorThresholdConfig(sensor_id="PRESS-01", min_value=1.5, max_value=8.0)

    event = await service.evaluate_reading(sensor_id="PRESS-01", value=0.8, config=config)

    assert event is not None
    assert event.rule == "MIN_EXCEEDED"
    assert event.value == 0.8
    assert len(service.get_anomalies("PRESS-01")) == 1


@pytest.mark.anyio
async def test_ocp_multiple_alert_strategies() -> None:
    """Demuestra OCP: se añade Webhook sin modificar la lógica del servicio."""
    log_strat = LogAlertStrategy()
    webhook_strat = WebhookAlertStrategy("https://webhook.internal/alert")
    service = AnomalyDetectionService(strategies=[log_strat, webhook_strat])

    config = SensorThresholdConfig(sensor_id="FLOW-01", max_value=100.0)
    await service.evaluate_reading(sensor_id="FLOW-01", value=130.0, config=config)

    assert len(log_strat.sent_alerts) == 1
    assert len(webhook_strat.sent_alerts) == 1
    assert webhook_strat.sent_alerts[0].sensor_id == "FLOW-01"


@pytest.mark.anyio
async def test_strategy_failure_resilience() -> None:
    """Verifica que una falla en una estrategia no bloquee a las demás ni al flujo principal."""

    class BrokenStrategy:
        async def send_alert(self, event) -> bool:
            raise RuntimeError("Falla de conexión al servicio de alerta")

    broken = BrokenStrategy()
    log_strat = LogAlertStrategy()
    service = AnomalyDetectionService(strategies=[broken, log_strat])

    config = SensorThresholdConfig(sensor_id="VIB-01", max_value=10.0)
    event = await service.evaluate_reading(sensor_id="VIB-01", value=15.0, config=config)

    assert event is not None
    assert len(log_strat.sent_alerts) == 1
