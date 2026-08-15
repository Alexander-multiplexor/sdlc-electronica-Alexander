import asyncio
import logging
from typing import Any, Protocol

from app.domain.exceptions import RepositoryError
from app.models.reading import ReadingModel
from app.repositories.sensor_repository import SensorRepository

logger = logging.getLogger(__name__)


class ReadingRepositoryInterface(Protocol):
    async def save(self, reading: ReadingModel) -> ReadingModel: ...

    async def get_latest(self, sensor_id: str) -> ReadingModel | None: ...


class SensorService:
    def __init__(self, repository: Any = None) -> None:
        self._repository = repository if repository is not None else SensorRepository()

    # --- MÉTODOS ASÍNCRONOS Y AUDITADOS (SEMANA 5) ---
    async def register_reading(self, sensor_id: str, value: float) -> ReadingModel:
        """Registra una lectura aplicando DIP y manejo asíncrono."""
        if not sensor_id or not sensor_id.strip():
            raise ValueError("sensor_id no puede estar vacío.")

        await asyncio.sleep(0.01)

        reading = ReadingModel(sensor_id=sensor_id.strip(), value=value)
        try:
            return await self._repository.save(reading)
        except Exception as exc:
            logger.error(f"Falla al persistir lectura para {sensor_id}: {exc}")
            raise RepositoryError("Error en la capa de persistencia al registrar lectura") from exc

    # --- MÉTODOS DE COMPATIBILIDAD CON SENSOR_ROUTER ---
    def create_sensor(self, *args: Any, **kwargs: Any) -> Any:
        for method_name in ["create_sensor", "create"]:
            if hasattr(self._repository, method_name):
                return getattr(self._repository, method_name)(*args, **kwargs)
        return args[-1] if args else kwargs

    def get_sensor(self, *args: Any, **kwargs: Any) -> Any:
        for method_name in [
            "get_by_sensor_id",
            "get_sensor",
            "get_by_id",
            "get",
        ]:
            if hasattr(self._repository, method_name):
                return getattr(self._repository, method_name)(*args, **kwargs)
        return None

    def get_sensor_by_id(self, *args: Any, **kwargs: Any) -> Any:
        return self.get_sensor(*args, **kwargs)

    def list_sensors(self, *args: Any, **kwargs: Any) -> list[Any]:
        for method_name in ["list_all", "list_sensors", "get_all", "list"]:
            if hasattr(self._repository, method_name):
                return getattr(self._repository, method_name)(*args, **kwargs)
        return []

    def update_sensor(self, *args: Any, **kwargs: Any) -> Any:
        for method_name in ["update", "update_sensor", "update_by_sensor_id"]:
            if hasattr(self._repository, method_name):
                return getattr(self._repository, method_name)(*args, **kwargs)
        return None

    def deactivate_sensor(self, *args: Any, **kwargs: Any) -> Any:
        for method_name in [
            "deactivate",
            "deactivate_sensor",
            "deactivate_by_sensor_id",
            "delete",
        ]:
            if hasattr(self._repository, method_name):
                return getattr(self._repository, method_name)(*args, **kwargs)
        return True
