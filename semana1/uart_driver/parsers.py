from abc import ABC, abstractmethod
from typing import Any


class MessageParser(ABC):
    """Clase Abstracta Base (ABC) que define el contrato para cualquier protocolo UART."""

    @abstractmethod
    def can_parse(self, data: bytes) -> bool:
        """Determina si la trama de bytes entrante pertenece a este protocolo."""
        pass

    @abstractmethod
    def parse(self, data: bytes) -> dict[str, Any]:
        """Decodifica la trama de bytes y extrae la información en un diccionario."""
        pass


class ModbusParser(MessageParser):
    """Parser para tramas industriales Modbus RTU."""

    def can_parse(self, data: bytes) -> bool:
        # Una trama Modbus RTU mínima estándar tiene al menos 4 bytes (ID, Función, Datos, CRC)
        # Para esta simulación, asumimos que si no es NMEA y tiene tamaño válido, la evaluamos
        return len(data) >= 4 and not data.startswith(b"$")

    def parse(self, data: bytes) -> dict[str, Any]:
        if not self.can_parse(data):
            raise ValueError("Trama inválida o corrupta para el protocolo Modbus RTU.")
        
        # Simulación de desempaquetado de bytes (estilo struct de C)
        slave_id = int(data[0])
        function_code = int(data[1])
        # Simulamos la lectura de un registro de sujeción (Holding Register) de un sensor
        valor_sensor = float(len(data) * 1.5) 
        
        return {
            "protocolo": "Modbus RTU",
            "slave_id": slave_id,
            "function_code": function_code,
            "value": valor_sensor
        }


class NMEAParser(MessageParser):
    """Parser para sentencias de geolocalización NMEA ($GPGGA)."""

    def can_parse(self, data: bytes) -> bool:
        # Las sentencias NMEA siempre inician con el carácter '$' y son cadenas ASCII
        return data.startswith(b"$GPGGA")

    def parse(self, data: bytes) -> dict[str, Any]:
        if not self.can_parse(data):
            raise ValueError("La trama no coincide con una sentencia válida NMEA $GPGGA.")
        
        try:
            # Convertimos los bytes a string ASCII y removemos saltos de línea
            cadena = data.decode("ascii").strip()
            componentes = cadena.split(",")
            
            # Una sentencia $GPGGA estándar tiene campos separados por comas (ID, Tiempo, Latitud, N/S, Longitud...)
            if len(componentes) < 6:
                raise ValueError("Sentencia NMEA incompleta.")
                
            return {
                "protocolo": "NMEA",
                "tipo": componentes[0],             # $GPGGA
                "timestamp": componentes[1],        # Hora UTC
                "latitud": componentes[2],          # Valor de latitud
                "longitud": componentes[4]          # Valor de longitud
            }
        except Exception as e:
            raise ValueError(f"Error decodificando sentencia NMEA: {e}")