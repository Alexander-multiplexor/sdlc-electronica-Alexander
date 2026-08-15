from typing import Any


class SensorNotFoundError(Exception):
    """Excepción lanzada cuando un sensor no está registrado."""

    pass


class SensorRegistry:
    def __init__(self) -> None:
        self._sensors: dict[str, dict[str, Any]] = {}

    def register(self, sensor_id: str, sensor_type: str, location: str) -> None:
        self._sensors[sensor_id] = {"id": sensor_id, "type": sensor_type, "location": location, "status": "ACTIVO"}

    def get(self, sensor_id: str) -> dict[str, Any]:
        if sensor_id not in self._sensors:
            raise SensorNotFoundError(f"El sensor '{sensor_id}' no existe.")
        return self._sensors[sensor_id]
