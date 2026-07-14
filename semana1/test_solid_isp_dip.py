import pytest
from semana1.solid_isp_dip import (
    Readable, BasicTemperatureSensor,
    DataRepository, DataProcessor, SensorReading
)

# =====================================================================
# TESTS: ISP
# =====================================================================
def test_isp_sensor_implements_readable():
    sensor = BasicTemperatureSensor()
    # Verificamos que cumple con el contrato de lectura
    assert isinstance(sensor, Readable)
    assert sensor.read() == 22.4

def test_isp_sensor_does_not_have_unnecessary_methods():
    sensor = BasicTemperatureSensor()
    # Validamos que no esté obligado a cargar con lógica de escritura
    assert not hasattr(sensor, 'write')


# =====================================================================
# TESTS: DIP
# =====================================================================
class InMemoryRepository(DataRepository):
    """Un repositorio falso (Mock) para pruebas unitarias rápidas[cite: 1]."""
    def __init__(self) -> None:
        self.storage = []
    
    def save(self, reading: SensorReading) -> None:
        self.storage.append(reading)
        
    def get_all(self) -> list[SensorReading]:
        return self.storage

def test_dip_processor_saves_valid_reading():
    # En el test inyectamos el repositorio seguro en memoria[cite: 1]
    repo = InMemoryRepository()
    processor = DataProcessor(repository=repo)
    
    reading = SensorReading("DHT22", 28.2)
    processor.process_and_store(reading)
    
    assert len(repo.get_all()) == 1
    assert repo.get_all()[0].sensor_id == "DHT22"

def test_dip_processor_ignores_invalid_reading():
    repo = InMemoryRepository()
    processor = DataProcessor(repository=repo)
    
    # Lectura inválida (por debajo o igual a cero en nuestra lógica de negocio)
    reading = SensorReading("DHT22", -5.0)
    processor.process_and_store(reading)
    
    assert len(repo.get_all()) == 0