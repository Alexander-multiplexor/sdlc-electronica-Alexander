from datetime import datetime, timezone

from sqlalchemy import Boolean, DateTime, Float, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db import Base


class SensorModel(Base):
    __tablename__ = "sensors"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    # sensor_id de negocio único (ej. "TEMP-01")
    sensor_id: Mapped[str] = mapped_column(String(50), unique=True, index=True, nullable=False)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    sensor_type: Mapped[str] = mapped_column(String(50), nullable=False)  # "TEMPERATURE", "HUMIDITY", "PRESSURE"
    location: Mapped[str] = mapped_column(String(100), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

    # Relación un sensor -> muchas lecturas
    readings: Mapped[list["ReadingModel"]] = relationship(
        back_populates="sensor", 
        cascade="all, delete-orphan"
    )


class ReadingModel(Base):
    __tablename__ = "readings"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    # Llave foránea que referencia al sensor_id único
    sensor_id: Mapped[str] = mapped_column(
        String(50), 
        ForeignKey("sensors.sensor_id", ondelete="CASCADE"), 
        index=True, 
        nullable=False
    )
    value: Mapped[float] = mapped_column(Float, nullable=False)
    unit: Mapped[str] = mapped_column(String(20), nullable=False)  # "C", "%", "hPa", etc.
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

    # Relación inversa
    sensor: Mapped["SensorModel"] = relationship(back_populates="readings")