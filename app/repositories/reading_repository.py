from collections.abc import Sequence
from datetime import datetime

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.sensor_hub import ReadingModel
from app.schemas.reading import ReadingCreate


class ReadingRepository:
    def create(self, db: Session, reading_in: ReadingCreate) -> ReadingModel:
        """Registra una lectura individual para un sensor."""
        db_reading = ReadingModel(sensor_id=reading_in.sensor_id, value=reading_in.value, unit=reading_in.unit)
        db.add(db_reading)
        db.commit()
        db.refresh(db_reading)
        return db_reading

    def list_by_sensor(
        self,
        db: Session,
        sensor_id: str,
        limit: int = 50,
        offset: int = 0,
        from_date: datetime | None = None,
        to_date: datetime | None = None,
    ) -> Sequence[ReadingModel]:
        """Consulta lecturas con paginación y filtro por rango de fechas."""
        stmt = select(ReadingModel).where(ReadingModel.sensor_id == sensor_id)

        # Filtros opcionales por fecha
        if from_date:
            stmt = stmt.where(ReadingModel.created_at >= from_date)
        if to_date:
            stmt = stmt.where(ReadingModel.created_at <= to_date)

        # Ordenar cronológicamente descendente + paginación (limit y offset)
        stmt = stmt.order_by(ReadingModel.created_at.desc()).offset(offset).limit(limit)
        return db.scalars(stmt).all()
