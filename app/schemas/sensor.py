from datetime import datetime
from enum import Enum

from pydantic import BaseModel, ConfigDict, Field


class SensorType(str, Enum):
    TEMPERATURE = "TEMPERATURE"
    HUMIDITY = "HUMIDITY"
    PRESSURE = "PRESSURE"


# Esquema base con campos comunes
class SensorBase(BaseModel):
    sensor_id: str = Field(
        ...,
        min_length=3,
        max_length=50,
        description="Identificador único del sensor (ej. TEMP-01)",
        examples=["TEMP-01"],
    )
    name: str = Field(..., min_length=2, max_length=100, examples=["Sensor Bodega 1"])
    sensor_type: SensorType = Field(..., description="Tipo de sensor soportado")
    location: str = Field(..., min_length=2, max_length=100, examples=["Nave Industrial A"])


# Para crear un sensor (solicitud POST)
class SensorCreate(SensorBase):
    pass


# Para actualizar parcialmente un sensor (solicitud PATCH)
class SensorUpdate(BaseModel):
    name: str | None = Field(None, min_length=2, max_length=100)
    location: str | None = Field(None, min_length=2, max_length=100)
    is_active: bool | None = None


# Para devolver la respuesta al cliente (salida GET/POST)
class SensorResponse(SensorBase):
    id: int
    is_active: bool
    created_at: datetime

    # Permite convertir automáticamente un modelo de SQLAlchemy a Pydantic
    model_config = ConfigDict(from_attributes=True)
