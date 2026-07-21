from dataclasses import dataclass
from typing import Protocol, runtime_checkable


@dataclass(frozen=True)
class SensorReading:
    sensor_id: str
    value: float

# =====================================================================
# 4. INTERFACE SEGREGATION PRINCIPLE (ISP)
# =====================================================================

# ❌ MAL: Una interfaz gorda que obliga a un sensor de solo lectura a implementar métodos que no necesita.
class BadSensorInterface:
    def read(self) -> float:
        pass
    def write(self, data: bytes) -> None:
        pass
    def calibrate(self) -> None:
        pass

@runtime_checkable # Decorador
#  BIEN: Dividimos la interfaz en componentes específicos usando Protocol (interfaces implícitas).
class Readable(Protocol):
    def read(self) -> float:
        ...

class Writable(Protocol):
    def write(self, data: bytes) -> None:
        ...

# Un sensor básico de temperatura solo implementa lo que realmente necesita
class BasicTemperatureSensor(Readable):
    def read(self) -> float:
        return 22.4


# =====================================================================
# 5. DEPENDENCY INVERSION PRINCIPLE (DIP)
# =====================================================================

# ❌ MAL: El procesador depende directamente de una base de datos de bajo nivel (PostgreSQL). No se puede testear sin la BD real.
class BadDataProcessor:
    def __init__(self) -> None:
        # Acoplamiento duro a una infraestructura específica
        self.database = "RealPostgreSQLConnection" 

#  BIEN: El procesador depende de una abstracción, no de la implementación concreta.
class DataRepository(Protocol):
    """Interfaz abstracta del repositorio de datos."""
    def save(self, reading: SensorReading) -> None:
        ...
    def get_all(self) -> list[SensorReading]:
        ...

class DataProcessor:
    """Depende enteramente de la abstracción mediante inyección de dependencias."""
    def __init__(self, repository: DataRepository) -> None:
        self._repo = repository  # Inyección de dependencias

    def process_and_store(self, reading: SensorReading) -> None:
        # Lógica de negocio simulada y almacenamiento abstracto
        if reading.value > 0:
            self._repo.save(reading)