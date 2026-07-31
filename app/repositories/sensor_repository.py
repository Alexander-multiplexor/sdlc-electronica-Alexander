from collections.abc import Sequence

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.sensor_hub import SensorModel
from app.schemas.sensor import SensorCreate, SensorUpdate


class SensorRepository:
    def create(self, db: Session, sensor_in: SensorCreate) -> SensorModel:
        """Crea y persiste un nuevo sensor en la base de datos."""
        db_sensor = SensorModel(
            sensor_id=sensor_in.sensor_id,
            name=sensor_in.name,
            sensor_type=sensor_in.sensor_type.value,
            location=sensor_in.location,
            is_active=True
        )
        db.add(db_sensor)
        db.commit()
        db.refresh(db_sensor)
        return db_sensor

    def get_by_sensor_id(self, db: Session, sensor_id: str) -> SensorModel | None:
        """Obtiene un sensor por su sensor_id de negocio (ej. 'TEMP-01')."""
        stmt = select(SensorModel).where(SensorModel.sensor_id == sensor_id)
        return db.scalar(stmt)

    def list_all(
        self, db: Session, limit: int = 50, offset: int = 0
    ) -> Sequence[SensorModel]:
        """Lista todos los sensores con soporte de paginación."""
        stmt = select(SensorModel).offset(offset).limit(limit)
        return db.scalars(stmt).all()

    def update(
        self, db: Session, sensor_id: str, sensor_update: SensorUpdate
    ) -> SensorModel | None:
        """Actualiza parcialmente la información de un sensor."""
        db_sensor = self.get_by_sensor_id(db, sensor_id)
        if not db_sensor:
            return None

        update_data = sensor_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_sensor, field, value)

        db.commit()
        db.refresh(db_sensor)
        return db_sensor

    def deactivate(self, db: Session, sensor_id: str) -> SensorModel | None:
        """Desactiva un sensor (borrado lógico para producción)."""
        db_sensor = self.get_by_sensor_id(db, sensor_id)
        if not db_sensor:
            return None

        db_sensor.is_active = False
        db.commit()
        db.refresh(db_sensor)
        return db_sensor