from collections.abc import Sequence
from datetime import datetime

from sqlalchemy.orm import Session

from app.models.sensor_hub import ReadingModel
from app.repositories.reading_repository import ReadingRepository
from app.repositories.sensor_repository import SensorRepository
from app.schemas.reading import ReadingCreate
from app.services.exceptions import (
    SensorInactiveError,
    SensorNotFoundError,
    SensorTypeMismatchError,
)


class ReadingService:
    def __init__(
        self,
        reading_repo: ReadingRepository | None = None,
        sensor_repo: SensorRepository | None = None,
    ) -> None:
        self.reading_repo = reading_repo or ReadingRepository()
        self.sensor_repo = sensor_repo or SensorRepository()

    def record_reading(self, db: Session, reading_in: ReadingCreate) -> ReadingModel:
        """
        Registra una lectura aplicando reglas de negocio:
        1. Que el sensor exista (HTTP 404 si no existe).
        2. Que el sensor esté activo (HTTP 400 si está inactivo).
        3. Que el tipo de sensor de la lectura coincida con el sensor registrado (HTTP 400).
        """
        sensor = self.sensor_repo.get_by_sensor_id(db, reading_in.sensor_id)
        if not sensor:
            raise SensorNotFoundError(reading_in.sensor_id)

        if not sensor.is_active:
            raise SensorInactiveError(reading_in.sensor_id)

        if sensor.sensor_type != reading_in.sensor_type.value:
            raise SensorTypeMismatchError(
                expected_type=sensor.sensor_type,
                received_type=reading_in.sensor_type.value,
            )

        return self.reading_repo.create(db, reading_in)

    def list_readings_for_sensor(
        self,
        db: Session,
        sensor_id: str,
        limit: int = 50,
        offset: int = 0,
        from_date: datetime | None = None,
        to_date: datetime | None = None,
    ) -> Sequence[ReadingModel]:
        """Obtiene el historial de lecturas validando que el sensor exista."""
        # Verificar existencia del sensor primero
        sensor = self.sensor_repo.get_by_sensor_id(db, sensor_id)
        if not sensor:
            raise SensorNotFoundError(sensor_id)

        return self.reading_repo.list_by_sensor(
            db,
            sensor_id=sensor_id,
            limit=limit,
            offset=offset,
            from_date=from_date,
            to_date=to_date,
        )
