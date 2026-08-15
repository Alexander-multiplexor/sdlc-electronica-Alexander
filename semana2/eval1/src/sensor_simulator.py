import random

from semana2.eval1.src.sensor_reading import SensorReading


class SensorSimulator:
    """Simulador de flota de sensores IoT utilizando distribución gaussiana."""

    def __init__(
        self,
        num_sensors: int = 10,
        temp_mean: float = 25.0,
        temp_std: float = 5.0,
        hum_mean: float = 50.0,
        hum_std: float = 15.0,
    ) -> None:
        self.sensor_ids = [f"SENSOR-{i + 1:02d}" for i in range(num_sensors)]
        self.temp_mean = temp_mean
        self.temp_std = temp_std
        self.hum_mean = hum_mean
        self.hum_std = hum_std

    def generate_cycle(self) -> list[SensorReading]:
        """Genera un ciclo de lecturas para todos los sensores de la flota."""
        readings = []
        for s_id in self.sensor_ids:
            # Generación gaussiana de temperatura y humedad
            temp = random.gauss(self.temp_mean, self.temp_std)
            hum = random.gauss(self.hum_mean, self.hum_std)

            # Acotar a valores dentro del rango físico de SensorReading
            temp_clamped = max(-40.0, min(80.0, temp))
            hum_clamped = max(0.0, min(100.0, hum))

            readings.append(
                SensorReading(
                    sensor_id=s_id,
                    temperature=round(temp_clamped, 2),
                    humidity=round(hum_clamped, 2),
                )
            )
        return readings
