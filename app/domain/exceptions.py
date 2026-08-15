"""Excepciones de dominio para SensorHub."""


class SensorHubError(Exception):
    """Excepción base de dominio."""

    pass


class RepositoryError(SensorHubError):
    """Error originado en la capa de persistencia/infraestructura."""

    pass


class SensorNotFoundError(SensorHubError):
    """Sensor no encontrado en el sistema."""

    pass