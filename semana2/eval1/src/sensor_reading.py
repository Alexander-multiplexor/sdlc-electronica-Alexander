from dataclasses import dataclass

@dataclass(frozen=True)
class SensorReading:
    sensor_id: str
    temperature: float
    humidity: float

    def __post_init__(self) -> None:
        if not (-50.0 <= self.temperature <= 100.0):
            raise ValueError(f"Temperatura fuera de rango permitido (-50 a 100 °C): {self.temperature}")
        if not (0.0 <= self.humidity <= 100.0):
            raise ValueError(f"Humedad fuera de rango permitido (0 a 100 %): {self.humidity}")