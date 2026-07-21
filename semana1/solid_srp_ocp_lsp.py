from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass(frozen=True)
class SensorReading:
    sensor_id: str
    value: float

# =====================================================================
# 1. SINGLE RESPONSIBILITY PRINCIPLE (SRP)
# =====================================================================

# ❌ MAL: La clase lee del hardware y también se encarga de la persistencia (dos razones para cambiar).
class BadSensorManager:
    def read_hardware(self) -> SensorReading:
        return SensorReading("TEMP-01", 24.5)
    
    def save_to_file(self, reading: SensorReading) -> None:
        # Simulación de escritura en archivo de texto
        pass

#  BIEN: Separamos las tareas. Una clase lee y otra persiste.
class SensorReader:
    """Su única responsabilidad es interactuar con el origen de los datos."""
    def read_hardware(self) -> SensorReading:
        return SensorReading("TEMP-01", 24.5)

class DataLogger:
    """Su única responsabilidad es la persistencia de la información."""
    def save(self, reading: SensorReading) -> None:
        # Simulación de persistencia pura
        pass


# =====================================================================
# 2. OPEN/CLOSED PRINCIPLE (OCP)
# =====================================================================

# ❌ MAL: Si mañana queremos agregar "EmailAlert", tenemos que modificar la clase existente (rompe OCP).
class BadAnomalyDetector:
    def check(self, reading: SensorReading, alert_type: str) -> None:
        if reading.value > 30.0:
            if alert_type == "console":
                print(f"Alerta en consola: {reading.sensor_id}")
            elif alert_type == "file":
                # Escribir en archivo
                pass

#  BIEN: Extendible mediante abstracciones sin modificar el detector original.
class AlertStrategy(ABC):
    @abstractmethod
    def send(self, message: str) -> None:
        pass

class ConsoleAlert(AlertStrategy):
    def send(self, message: str) -> None:
        print(f"Consola: {message}")

class FileAlert(AlertStrategy):
    def send(self, message: str) -> None:
        # Escritura simulada en archivo
        pass

class AnomalyDetector:
    """Abierto a la extensión, cerrado a la modificación."""
    def __init__(self, alert: AlertStrategy, threshold: float) -> None:
        self._alert = alert
        self._threshold = threshold
        
    def check(self, reading: SensorReading) -> None:
        if reading.value > self._threshold:
            self._alert.send(f"Anomalía en {reading.sensor_id}")


# =====================================================================
# 3. LISKOV SUBSTITUTION PRINCIPLE (LSP)
# =====================================================================

class BaseSensor(ABC):
    @abstractmethod
    def read(self) -> float:
        pass

# ❌ MAL: Altera drásticamente el comportamiento esperado arrojando excepciones inesperadas o alterando tipos.
class BrokenSensor(BaseSensor):
    def read(self) -> float:
        # Rompe el contrato porque requiere una verificación externa obligatoria o lanza errores letales
        raise RuntimeError("Sensor no calibrado. ¡Programa abortado!")

#  BIEN: Las subclases son perfectamente intercambiables sin romper la función cliente[cite: 1, 2].
class TemperatureSensor(BaseSensor):
    def read(self) -> float:
        return 25.3

class HumiditySensor(BaseSensor):
    def read(self) -> float:
        return 60.1

def process_sensor(sensor: BaseSensor) -> float:
    """Esta función cliente funciona de forma transparente con cualquier subclase válida[cite: 1, 2]."""
    return sensor.read()