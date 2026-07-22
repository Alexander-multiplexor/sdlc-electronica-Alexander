import json
from typing import Any


class DataRecorder:
    """Su única responsabilidad es la persistencia pura de los datos parseados en archivos (SRP)."""
    
    def __init__(self, output_path: str) -> None:
        self._output_path = output_path

    def record(self, data: dict[str, Any]) -> None:
        """Escribe una línea de datos en formato JSON agregándola al final del archivo destino."""
        # El modo 'a' (append) agrega datos al final del archivo sin borrar el contenido previo
        with open(self._output_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(data) + "\n")