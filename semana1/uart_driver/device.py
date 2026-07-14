from typing import Any, Dict
from semana1.uart_driver.config import UartConfig
from semana1.uart_driver.parsers import MessageParser

class UartDevice:
    """Dispositivo UART central que demuestra el Principio de Inversión de Dependencias (DIP)."""
    
    def __init__(self, config: UartConfig, parser: MessageParser) -> None:
        self._config = config
        self._parser = parser  # Inyección de la abstracción del parser
        self._connected = False

    @property
    def is_connected(self) -> bool:
        """Expone de forma segura si el puerto serial simulado está abierto."""
        return self._connected

    def connect(self) -> None:
        """Simula la apertura y configuración del puerto serial físico."""
        self._connected = True

    def disconnect(self) -> None:
        """Simula el cierre del puerto serial y liberación del bus."""
        self._connected = False

    def read_and_parse(self, raw_data: bytes) -> Dict[str, Any]:
        """Lee una trama cruda del buffer y delega el procesamiento al parser inyectado."""
        if not self._connected:
            raise RuntimeError("Error de E/S: El dispositivo UART no está conectado.")
        
        # El dispositivo no sabe qué protocolo es, solo invoca la abstracción inyectada
        return self._parser.parse(raw_data)