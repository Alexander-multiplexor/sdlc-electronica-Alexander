# Semana 5 · Prompting Efectivo: Pobre vs. Estructurado

Este documento evalúa 3 tareas reales del sistema **SensorHub**, contrastando un prompt ambiguo (pobre) contra un prompt con contexto, restricciones y formato estricto (bueno).

---

## Tarea 1: Función de calibración de lectura ADC

### 🔴 Prompt Pobre
> "Haz una función en Python para convertir valores de sensor."

#### Resultado del Prompt Pobre
```python
def convertir(val):
    v = (val / 1023) * 5.0
    temp = v * 100
    return temp
```

- Deficiencias: Asume hardware arbitrario (10 bits, 5V), carece de type hints, no valida valores negativos ni desbordamientos de rango, no incluye docstring.

### 🟢 Prompt Bueno (Estructurado)

CONTEXTO: Sistema SensorHub (Python 3.12, FastAPI). Módulo de adquisición de señales.
TAREA: Escribe una función pura `raw_to_calibrated_voltage` en `semana5/conversions.py` que convierta un valor digital ADC de N-bits a voltaje y aplique calibración lineal (gain y offset).
RESTRICCIONES:
- Type hints estrictos (mypy compliant).
- Docstring en formato Google con precondiciones y postcondiciones.
- Validar que `raw_value` no sea negativo y no exceda `(2**adc_bits) - 1`. Si excede, lanzar `ValueError`.
- Sin dependencias externas; usar biblioteca estándar.
- Redondeo a 4 decimales.
ENTREGA: Solo el código de la función con su import correspondiente.

#### Resultado del Prompt Bueno
```python
def raw_to_calibrated_voltage(
    raw_value: int,
    v_ref: float = 3.3,
    adc_bits: int = 12,
    gain: float = 1.0,
    offset: float = 0.0,
) -> float:
    """Convierte una lectura digital ADC a voltaje calibrado.

    Args:
        raw_value: Valor entero del convertidor analógico-digital.
        v_ref: Voltaje de referencia del ADC en voltios.
        adc_bits: Resolución en bits del convertidor ADC.
        gain: Factor de escala lineal (ganancia de calibración).
        offset: Desplazamiento lineal en voltios.

    Returns:
        float: Voltaje calculado y calibrado redondeado a 4 decimales.

    Raises:
        ValueError: Si raw_value es negativo o supera el rango de resolución.
    """
    max_raw = (1 << adc_bits) - 1
    if not (0 <= raw_value <= max_raw):
        raise ValueError(
            f"raw_value ({raw_value}) fuera de rango para resolución de {adc_bits} bits [0, {max_raw}]."
        )

    voltage_ideal = (raw_value / max_raw) * v_ref
    voltage_calibrated = (voltage_ideal * gain) + offset
    return round(voltage_calibrated, 4)
```

## Tarea 2: Consulta de agregación en Repositorio (SQLAlchemy 2.0)

### 🔴 Prompt Pobre
> "Hazme una query en SQLAlchemy para sacar el promedio de lecturas por sensor."

#### Resultado del Prompt Pobre
```python
def get_promedios(db, sensor_id):
    return db.query(func.avg(Reading.value)).filter(Reading.sensor_id == sensor_id).scalar()
```

- Deficiencias: Utiliza la API legacy db.query obsoleta en SQLAlchemy 2.x, omite el soporte asíncrono (AsyncSession) y no maneja sensores sin lecturas.

### 🟢 Prompt Bueno (Estructurado)

CONTEXTO: SensorHub backend (FastAPI, Python 3.12, SQLAlchemy 2.0+ con AsyncSession).
Modelo de datos: `ReadingModel(id: int, sensor_id: str, value: float, timestamp: datetime)`.
TAREA: Escribe el método asíncrono `get_sensor_statistics` dentro de `SQLAlchemyReadingRepository`.
RESTRICCIONES:
- Usa la sintaxis SQLAlchemy 2.0 (`select(func.avg(...), func.min(...), func.max(...))`).
- Retorna un Value Object tipado `SensorStats(avg: float | None, min: float | None, max: float | None, count: int)`.
- Manejar `AsyncSession` con type hints estrictos.
- Sin llamadas síncronas bloqueantes.
ENTREGA: Código del método y del dataclass `SensorStats`.

#### Resultado del Prompt Bueno
```python
from dataclasses import dataclass
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.reading import ReadingModel


@dataclass(frozen=True)
class SensorStats:
    sensor_id: str
    avg_value: float | None
    min_value: float | None
    max_value: float | None
    count: int


class SQLAlchemyReadingRepository:

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_sensor_statistics(self, sensor_id: str) -> SensorStats:
        stmt = select(
            func.avg(ReadingModel.value).label("avg_val"),
            func.min(ReadingModel.value).label("min_val"),
            func.max(ReadingModel.value).label("max_val"),
            func.count(ReadingModel.id).label("count_val"),
        ).where(ReadingModel.sensor_id == sensor_id)

        result = await self._session.execute(stmt)
        row = result.one()

        return SensorStats(
            sensor_id=sensor_id,
            avg_value=round(row.avg_val, 2) if row.avg_val is not None else None,
            min_value=round(row.min_val, 2) if row.min_val is not None else None,
            max_value=round(row.max_val, 2) if row.max_val is not None else None,
            count=row.count_val or 0,
        )
```

## Tarea 3: Detección de umbrales con Estrategias Intercambiables (OCP)

### 🔴 Prompt Pobre
> "Crea un validador que mande alertas si el sensor pasa un límite."

#### Resultado del Prompt Pobre
```python
def check_alert(sensor, val):
    if val > sensor.limit:
        print(f"Alerta en {sensor.name}!")
        import requests
        requests.post("[https://webhook.site/test](https://webhook.site/test)", json={"alert": val})
```

- Deficiencias: Viola SRP y OCP, llamadas HTTP acopladas y bloqueantes, imposible de probar con tests unitarios puros.

### 🟢 Prompt Bueno (Estructurado)

CONTEXTO: SensorHub Core Domain (Python 3.12). Arquitectura en Capas.
TAREA: Diseña un servicio de evaluación `AnomalyEvaluator` y la abstracción `AlertNotificationStrategy` utilizando `typing.Protocol` para aplicar OCP y DIP.
RESTRICCIONES:
- `AlertNotificationStrategy` debe ser un `Protocol` asíncrono con método `notify(event: AnomalyEvent) -> bool`.
- `AnomalyEvaluator` evalúa si el valor excede `max_limit` o es menor que `min_limit`.
- Recibe las estrategias mediante inyección de dependencias.
- Las fallas individuales de notificación no deben interrumpir el flujo principal.
ENTREGA: Código completo de las clases, protocolos y modelos de dominio.

#### Resultado del Prompt Bueno
```python
from dataclasses import dataclass
from datetime import datetime, timezone
import logging
from typing import Protocol

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class AnomalyEvent:
    sensor_id: str
    current_value: float
    threshold_limit: float
    violation_type: str  # "HIGH_THRESHOLD" | "LOW_THRESHOLD"
    timestamp: datetime


class AlertNotificationStrategy(Protocol):

    async def notify(self, event: AnomalyEvent) -> bool:
        ...


class AnomalyEvaluator:

    def __init__(self, strategies: list[AlertNotificationStrategy]) -> None:
        self._strategies = strategies

    async def evaluate_and_notify(
        self,
        sensor_id: str,
        value: float,
        min_limit: float | None = None,
        max_limit: float | None = None,
    ) -> AnomalyEvent | None:
        event: AnomalyEvent | None = None
        now = datetime.now(timezone.utc)

        if max_limit is not None and value > max_limit:
            event = AnomalyEvent(
                sensor_id=sensor_id,
                current_value=value,
                threshold_limit=max_limit,
                violation_type="HIGH_THRESHOLD",
                timestamp=now,
            )
        elif min_limit is not None and value < min_limit:
            event = AnomalyEvent(
                sensor_id=sensor_id,
                current_value=value,
                threshold_limit=min_limit,
                violation_type="LOW_THRESHOLD",
                timestamp=now,
            )

        if event:
            for strategy in self._strategies:
                try:
                    await strategy.notify(event)
                except Exception as exc:
                    logger.error(
                        f"Error en notificación de {strategy.__class__.__name__}: {exc}"
                    )

        return event
```