import json

from semana1.uart_driver.recorder import DataRecorder


def test_recorder_escribe_json_line_exitoso(tmp_path):
    """Test 1: Verifica que se guarde un registro correctamente en formato JSON-lines."""
    archivo_temporal = tmp_path / "sensor_data.jsonl"
    recorder = DataRecorder(str(archivo_temporal))
    
    datos_prueba = {"protocolo": "Modbus RTU", "slave_id": 1, "value": 24.5}
    recorder.record(datos_prueba)
    
    # Leemos el archivo generado para validar el formato de salida
    lineas = archivo_temporal.read_text().splitlines()
    assert len(lineas) == 1
    assert json.loads(lineas[0]) == datos_prueba

def test_recorder_guarda_multiples_lineas_secuenciales(tmp_path):
    """Test 2: Valida que agregue registros de forma secuencial sin sobrescribir los anteriores."""
    archivo_temporal = tmp_path / "telemetria.jsonl"
    recorder = DataRecorder(str(archivo_temporal))
    
    recorder.record({"id": 1, "msg": "Trama 1"})
    recorder.record({"id": 2, "msg": "Trama 2"})
    
    lineas = archivo_temporal.read_text().splitlines()
    assert len(lineas) == 2
    assert json.loads(lineas[0])["id"] == 1
    assert json.loads(lineas[1])["id"] == 2

def test_recorder_archivo_no_existe_inicialmente(tmp_path):
    """Test 3: Comprueba que el objeto no crea el archivo físicamente hasta realizar la primera escritura."""
    archivo_inactivo = tmp_path / "vacio.jsonl"
    assert not archivo_inactivo.exists()