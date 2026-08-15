# AI Code Review · Reporte de Revisión de Código Asistida

**Archivo auditado:** `app/services/sensor_service.py`  
**Rol asignado a la IA:** Ingeniero Senior de Software (Code Reviewer)  
**Objetivo:** Detectar violaciones de SOLID, casos borde no contemplados, riesgos de concurrencia/seguridad y sobreingeniería.

---

## 1. Tabla de Hallazgos y Decisiones

| ID | Ubicación | Categoría | Severidad | Hallazgo de la IA | Veredicto | Justificación Técnica |
|---|---|---|---|---|---|---|
| **H-01** | L45-L50 | Principios SOLID (DIP) | Alta | El servicio instancia directamente el repositorio `SQLAlchemyReadingRepository()`, acoplando la lógica de negocio a la base de datos. | **ACEPTADA** | Viola el Principio de Inversión de Dependencias (DIP). Se refactoriza para inyectar una abstracción `ReadingRepositoryInterface` (`typing.Protocol`). |
| **H-02** | L78 | Manejo de Excepciones | Media | Bloque `except Exception:` genérico que oculta errores reales y dificulta la trazabilidad. | **ACEPTADA** | Se capturan errores específicos de capa de persistencia y se encapsulan en excepciones de dominio (`RepositoryError`). |
| **H-03** | L102 | Rendimiento / Asincronía | Alta | Uso de `time.sleep(1)` para debounce de hardware dentro de un método `async`. | **ACEPTADA** | `time.sleep()` bloquea el Event Loop de asyncio para todos los clientes concurrentes. Se reemplaza por `asyncio.sleep()`. |
| **H-04** | L115 | Arquitectura / YAGNI | Baja | Sugerencia de incorporar Kafka/RabbitMQ para encolar cada lectura antes de guardarla. | **RECHAZADA** | **Sobreingeniería injustificada:** SensorHub opera como monolito modular. Introducir un broker distribuido añade costo operativo, latencia de red y complejidad de consistencia eventual innecesaria (*MonolithFirst*). |
| **H-05** | L130 | Seguridad / Alucinación | Baja | Señalamiento de posible vulnerabilidad SQL Injection en el uso de `session.scalars(select(ReadingModel).filter_by(sensor_id=sensor_id))`. | **RECHAZADA** | **Alucinación técnica de la IA:** SQLAlchemy 2.0 compila consultas parametrizadas internamente en el objeto `Select`. No existe interpolación de cadenas insegura. |

---

## 2. Refactor Implementado en `app/services/sensor_service.py`

```python
import asyncio
import logging
from typing import Protocol
from app.domain.exceptions import RepositoryError
from app.models.reading import ReadingModel

logger = logging.getLogger(__name__)


class ReadingRepositoryInterface(Protocol):
    async def save(self, reading: ReadingModel) -> ReadingModel: ...

    async def get_latest(self, sensor_id: str) -> ReadingModel | None: ...


class SensorService:
    def __init__(self, repository: ReadingRepositoryInterface) -> None:
        self._repository = repository

    async def register_reading(self, sensor_id: str, value: float) -> ReadingModel:
        if not sensor_id or not sensor_id.strip():
            raise ValueError("sensor_id no puede estar vacío.")

        # H-03: sleep no bloqueante para el event loop
        await asyncio.sleep(0.01)

        reading = ReadingModel(sensor_id=sensor_id.strip(), value=value)
        try:
            # H-01: DIP cumplido mediante inyección
            return await self._repository.save(reading)
        except Exception as exc:
            # H-02: Excepción encapsulada con causa original
            logger.error(f"Falla al persistir lectura para {sensor_id}: {exc}")
            raise RepositoryError("Error en la capa de persistencia al registrar lectura") from exc
```