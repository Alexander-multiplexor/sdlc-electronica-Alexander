from dataclasses import dataclass
from datetime import datetime


@dataclass
class ReadingModel:
    sensor_id: str
    value: float
    id: int | None = None
    timestamp: datetime | None = None
