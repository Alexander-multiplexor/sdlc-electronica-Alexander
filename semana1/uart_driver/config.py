from dataclasses import dataclass


@dataclass(frozen=True)
class UartConfig:
    baudrate: int
    parity: str = "N"  # 'N', 'E', 'O'
    stop_bits: int = 1  # 1, 2
    timeout: float = 1.0

    def __post_init__(self) -> None:
        """Valida las reglas físicas del puerto serial al instanciar el objeto."""
        # Validar baudrates estándar de electrónica
        baudrates_validos = [9600, 14400, 19200, 38400, 57600, 115200]
        if self.baudrate not in baudrates_validos:
            raise ValueError(f"Baudrate {self.baudrate} no soportado. Debe ser uno de: {baudrates_validos}")

        # Validar paridad
        if self.parity not in ["N", "E", "O"]:
            raise ValueError(f"Paridad '{self.parity}' inválida. Use 'N' (None), 'E' (Even) u 'O' (Odd)")
