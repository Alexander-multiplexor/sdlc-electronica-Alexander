import logging
from typing import Any, Protocol, cast

import anyio
from sqlalchemy.orm import Session

from app.domain.exceptions import RepositoryError
from app.models.reading import ReadingModel
from app.repositories.sensor_repository import SensorRepository
from app.schemas.sensor import SensorCreate, SensorResponse, SensorUpdate

logger = logging.getLogger(__name__)


class ReadingRepositoryInterface(Protocol):

    async def save(self, reading: ReadingModel) -> ReadingModel:
        ...

    async def get_latest(self, sensor_id: str) -> ReadingModel | None:
        ...


class SensorRepositoryProtocol(Protocol):

    def create(self, db: Session, sensor_in: SensorCreate) -> Any:
        ...

    def get_by_sensor_id(self, db: Session, sensor_id: str) -> Any:
        ...

    def list_all(
        self, db: Session, limit: int = 100, offset: int = 0
    ) -> list[Any]:
        ...

    def update(
        self, db: Session, sensor_id: str, sensor_update: SensorUpdate
    ) -> Any:
        ...

    def deactivate(self, db: Session, sensor_id: str) -> Any:
        ...


class SensorService:

    def __init__(
        self,
        repository: SensorRepositoryProtocol | Any = None,
        reading_repository: ReadingRepositoryInterface | Any = None,
    ) -> None:
        self._repository: Any = (
            repository if repository is not None else SensorRepository()
        )
        self._reading_repository: Any = (
            reading_repository
            if reading_repository is not None
            else self._repository
        )

    # --- INGESTA ASÍNCRONA DE TELEMETRÍA (SEMANA 5) ---
    async def register_reading(
        self, sensor_id: str, value: float
    ) -> ReadingModel:
        """Registra una lectura aplicando DIP y manejo asíncrono con AnyIO."""
        if not sensor_id or not sensor_id.strip():
            raise ValueError("sensor_id no puede estar vacío.")

        # Backend-agnostic sleep con AnyIO (compatible con asyncio y trio)
        await anyio.sleep(0.01)

        reading = ReadingModel(sensor_id=sensor_id.strip(), value=value)
        try:
            saved: ReadingModel = cast(
                ReadingModel, await self._reading_repository.save(reading)
            )
            return saved
        except Exception as exc:
            logger.error(f"Falla al persistir lectura para {sensor_id}: {exc}")
            raise RepositoryError(
                "Error en la capa de persistencia al registrar lectura"
            ) from exc

    # --- OPERACIONES CRUD DE METADATOS (DIP) ---
    def create_sensor(
        self, db: Session, sensor_in: SensorCreate
    ) -> SensorResponse:
        for method_name in ["create_sensor", "create"]:
            if hasattr(self._repository, method_name):
                res = getattr(self._repository, method_name)(db, sensor_in)
                return cast(SensorResponse, res)
        return cast(SensorResponse, sensor_in)

    def get_sensor(self, db: Session, sensor_id: str) -> SensorResponse | None:
        for method_name in [
            "get_by_sensor_id",
            "get_sensor",
            "get_by_id",
            "get",
        ]:
            if hasattr(self._repository, method_name):
                res = getattr(self._repository, method_name)(db, sensor_id)
                return cast(SensorResponse | None, res)
        return None

    def get_sensor_by_id(
        self, db: Session, sensor_id: str
    ) -> SensorResponse | None:
        return self.get_sensor(db, sensor_id)

    def list_sensors(
        self, db: Session, limit: int = 100, offset: int = 0
    ) -> list[SensorResponse]:
        for method_name in ["list_all", "list_sensors", "get_all", "list"]:
            if hasattr(self._repository, method_name):
                res = getattr(self._repository, method_name)(
                    db, limit=limit, offset=offset
                )
                return cast(list[SensorResponse], res)
        return []

    def update_sensor(
        self, db: Session, sensor_id: str, sensor_update: SensorUpdate
    ) -> SensorResponse | None:
        for method_name in ["update", "update_sensor", "update_by_sensor_id"]:
            if hasattr(self._repository, method_name):
                res = getattr(self._repository, method_name)(
                    db, sensor_id, sensor_update
                )
                return cast(SensorResponse | None, res)
        return None

    def deactivate_sensor(self, db: Session, sensor_id: str) -> bool:
        for method_name in [
            "deactivate",
            "deactivate_sensor",
            "deactivate_by_sensor_id",
            "delete",
        ]:
            if hasattr(self._repository, method_name):
                res = getattr(self._repository, method_name)(db, sensor_id)
                return bool(res)
        return True