"""Módulo de detección y notificación de anomalías en telemetría de sensores."""

from dataclasses import dataclass
from datetime import datetime, timezone
import logging
from typing import Protocol

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class AnomalyEvent:
    sensor_id: str
    value: float
    limit: float
    rule: str  # "MAX_EXCEEDED" | "MIN_EXCEEDED"
    timestamp: datetime


@dataclass(frozen=True)
class SensorThresholdConfig:
    sensor_id: str
    min_value: float | None = None
    max_value: float | None = None


class AlertNotificationStrategy(Protocol):
    """Contrato abstracto para estrategias de notificación de alertas (OCP)."""

    async def send_alert(self, event: AnomalyEvent) -> bool:
        ...


class LogAlertStrategy:
    """Estrategia de alerta que registra en logs del sistema."""

    def __init__(self) -> None:
        self.sent_alerts: list[AnomalyEvent] = []

    async def send_alert(self, event: AnomalyEvent) -> bool:
        self.sent_alerts.append(event)
        logger.warning(
            f"[ALERTA LOG] Sensor {event.sensor_id} violó umbral ({event.rule}): "
            f"Valor actual: {event.value}, Límite: {event.limit}"
        )
        return True


class WebhookAlertStrategy:
    """Estrategia de alerta vía HTTP Webhook simulado."""

    def __init__(self, endpoint_url: str) -> None:
        self._endpoint_url = endpoint_url
        self.sent_alerts: list[AnomalyEvent] = []

    async def send_alert(self, event: AnomalyEvent) -> bool:
        # En entorno real: await aiohttp.post(self._endpoint_url, json=...)
        self.sent_alerts.append(event)
        return True


class AnomalyDetectionService:
    """Servicio de detección de anomalías desacoplado de infraestructura."""

    def __init__(
        self,
        strategies: list[AlertNotificationStrategy] | None = None,
    ) -> None:
        self._strategies: list[AlertNotificationStrategy] = strategies or []
        self._registry: list[AnomalyEvent] = []

    def register_strategy(self, strategy: AlertNotificationStrategy) -> None:
        """Permite inyectar dinámicamente nuevas estrategias cumpliendo OCP."""
        self._strategies.append(strategy)

    def get_anomalies(
        self, sensor_id: str | None = None
    ) -> list[AnomalyEvent]:
        """Consulta el historial de anomalías registradas."""
        if sensor_id:
            return [a for a in self._registry if a.sensor_id == sensor_id]
        return list(self._registry)

    async def evaluate_reading(
        self, sensor_id: str, value: float, config: SensorThresholdConfig
    ) -> AnomalyEvent | None:
        """Evalúa una lectura contra los umbrales configurados."""
        event: AnomalyEvent | None = None
        now = datetime.now(timezone.utc)

        if config.max_value is not None and value > config.max_value:
            event = AnomalyEvent(
                sensor_id=sensor_id,
                value=value,
                limit=config.max_value,
                rule="MAX_EXCEEDED",
                timestamp=now,
            )
        elif config.min_value is not None and value < config.min_value:
            event = AnomalyEvent(
                sensor_id=sensor_id,
                value=value,
                limit=config.min_value,
                rule="MIN_EXCEEDED",
                timestamp=now,
            )

        if event:
            self._registry.append(event)
            for strategy in self._strategies:
                try:
                    await strategy.send_alert(event)
                except Exception as exc:
                    logger.error(
                        f"Falla en notificación con estrategia {strategy.__class__.__name__}: {exc}"
                    )

        return event