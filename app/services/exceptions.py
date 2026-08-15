class SensorNotFoundError(Exception):
    """Lanzada cuando un sensor no existe en la base de datos (HTTP 404)."""

    def __init__(self, sensor_id: str) -> None:
        self.sensor_id = sensor_id
        super().__init__(f"El sensor con ID '{sensor_id}' no fue encontrado.")


class SensorAlreadyExistsError(Exception):
    """Lanzada al intentar registrar un sensor_id duplicado (HTTP 409)."""

    def __init__(self, sensor_id: str) -> None:
        self.sensor_id = sensor_id
        super().__init__(f"El sensor con ID '{sensor_id}' ya existe en el sistema.")


class SensorInactiveError(Exception):
    """Lanzada al intentar registrar lecturas en un sensor desactivado (HTTP 400)."""

    def __init__(self, sensor_id: str) -> None:
        self.sensor_id = sensor_id
        super().__init__(f"El sensor con ID '{sensor_id}' se encuentra inactivo.")


class SensorTypeMismatchError(Exception):
    """Lanzada cuando la lectura no coincide con el tipo de sensor registrado (HTTP 400)."""

    def __init__(self, expected_type: str, received_type: str) -> None:
        self.expected_type = expected_type
        self.received_type = received_type
        super().__init__(f"Tipo de lectura '{received_type}' incompatible con el tipo del sensor '{expected_type}'.")
