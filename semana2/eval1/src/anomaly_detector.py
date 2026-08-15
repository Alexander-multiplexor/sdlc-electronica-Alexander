from semana2.eval1.src.sensor_reading import SensorReading


class AnomalyDetector:
    def __init__(self, max_temp: float = 35.0, max_humidity: float = 80.0) -> None:
        self.max_temp = max_temp
        self.max_humidity = max_humidity

    def evaluate(self, reading: SensorReading) -> tuple[bool, str]:
        reasons = []
        if reading.temperature > self.max_temp:
            reasons.append(f"TEMPERATURA_ALTA ({reading.temperature}°C > {self.max_temp}°C)")
        if reading.humidity > self.max_humidity:
            reasons.append(f"HUMEDAD_ALTA ({reading.humidity}% > {self.max_humidity}%)")

        if reasons:
            return True, " | ".join(reasons)
        return False, "NORMAL"
