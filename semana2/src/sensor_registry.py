class SensorNotFoundError(Exception):
    """Excepción lanzada cuando un sensor no está registrado."""
    pass


class SensorRegistry:
    def __init__(self) -> None:
        self._sensors: dict[str, dict[str, str]] = {}

    def get(self, sensor_id: str) -> dict[str, str]:
        if sensor_id not in self._sensors:
            raise SensorNotFoundError(f"El sensor '{sensor_id}' no existe.")
        return self._sensors[sensor_id]