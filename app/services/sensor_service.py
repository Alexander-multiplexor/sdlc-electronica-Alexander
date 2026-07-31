from collections.abc import Sequence

from sqlalchemy.orm import Session

from app.models.sensor_hub import SensorModel
from app.repositories.sensor_repository import SensorRepository
from app.schemas.sensor import SensorCreate, SensorUpdate
from app.services.exceptions import SensorAlreadyExistsError, SensorNotFoundError


class SensorService:
    def __init__(self, sensor_repo: SensorRepository | None = None) -> None:
        # Inyección de dependencias para facilitar los unit tests con mocks o fakes
        self.sensor_repo = sensor_repo or SensorRepository()

    def create_sensor(self, db: Session, sensor_in: SensorCreate) -> SensorModel:
        """Crea un nuevo sensor validando que no exista previamente (evita duplicados -> 409)."""
        existing = self.sensor_repo.get_by_sensor_id(db, sensor_in.sensor_id)
        if existing:
            raise SensorAlreadyExistsError(sensor_in.sensor_id)
        return self.sensor_repo.create(db, sensor_in)

    def get_sensor(self, db: Session, sensor_id: str) -> SensorModel:
        """Obtiene un sensor por su sensor_id (lanza 404 si no existe)."""
        sensor = self.sensor_repo.get_by_sensor_id(db, sensor_id)
        if not sensor:
            raise SensorNotFoundError(sensor_id)
        return sensor

    def list_sensors(
        self, db: Session, limit: int = 50, offset: int = 0
    ) -> Sequence[SensorModel]:
        """Lista todos los sensores registrados con soporte de paginación."""
        return self.sensor_repo.list_all(db, limit=limit, offset=offset)

    def update_sensor(
        self, db: Session, sensor_id: str, sensor_update: SensorUpdate
    ) -> SensorModel:
        """Actualiza parcialmente un sensor existente."""
        self.get_sensor(db, sensor_id)  # Lanza 404 si no existe
        updated_sensor = self.sensor_repo.update(db, sensor_id, sensor_update)
        if not updated_sensor:
            raise SensorNotFoundError(sensor_id)
        return updated_sensor

    def deactivate_sensor(self, db: Session, sensor_id: str) -> SensorModel:
        """Desactiva un sensor (borrado lógico para producción)."""
        self.get_sensor(db, sensor_id)  # Lanza 404 si no existe
        deactivated_sensor = self.sensor_repo.deactivate(db, sensor_id)
        if not deactivated_sensor:
            raise SensorNotFoundError(sensor_id)
        return deactivated_sensor