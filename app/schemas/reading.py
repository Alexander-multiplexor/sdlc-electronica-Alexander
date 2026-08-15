from datetime import datetime
from typing import TypedDict

from pydantic import BaseModel, ConfigDict, Field, model_validator

from app.schemas.sensor import SensorType


# Definimos la estructura exacta del diccionario para que mypy conozca sus tipos
class SensorPhysicsRule(TypedDict):
    valid_units: set[str]
    min_val: float
    max_val: float


# Anotamos explícitamente el tipo de PHYSICAL_LIMITS
PHYSICAL_LIMITS: dict[SensorType, SensorPhysicsRule] = {
    SensorType.TEMPERATURE: {
        "valid_units": {"C", "F", "K"},
        "min_val": -50.0,  # °C
        "max_val": 150.0,  # °C
    },
    SensorType.HUMIDITY: {
        "valid_units": {"%"},
        "min_val": 0.0,  # % HR
        "max_val": 100.0,  # % HR
    },
    SensorType.PRESSURE: {
        "valid_units": {"hPa", "bar"},
        "min_val": 300.0,  # hPa
        "max_val": 1100.0,  # hPa
    },
}


class ReadingCreate(BaseModel):
    sensor_id: str = Field(..., description="ID del sensor al que pertenece la lectura")
    value: float = Field(..., description="Valor medido por el sensor")
    unit: str = Field(..., description="Unidad de medida (ej. C, %, hPa)")
    sensor_type: SensorType = Field(..., description="Tipo de sensor para validar la física del valor")

    @model_validator(mode="after")
    def validate_physics(self) -> "ReadingCreate":
        """Valida que la unidad sea conocida y el valor esté dentro del rango físico del sensor."""
        rules = PHYSICAL_LIMITS.get(self.sensor_type)

        if not rules:
            raise ValueError(f"Tipo de sensor '{self.sensor_type}' no soportado para validación física.")

        # 1. Validar unidad de medida
        if self.unit not in rules["valid_units"]:
            raise ValueError(
                f"Unidad '{self.unit}' no válida para {self.sensor_type.value}. "
                f"Unidades permitidas: {list(rules['valid_units'])}"
            )

        # 2. Validar rango físico (normalizado para la regla)
        if not (rules["min_val"] <= self.value <= rules["max_val"]):
            raise ValueError(
                f"Valor {self.value} {self.unit} está fuera del rango físico "
                f"permitido [{rules['min_val']}, {rules['max_val']}] para {self.sensor_type.value}."
            )

        return self


class ReadingResponse(BaseModel):
    id: int
    sensor_id: str
    value: float
    unit: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
