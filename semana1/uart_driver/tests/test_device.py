import pytest
from semana1.uart_driver.config import UartConfig
from semana1.uart_driver.parsers import ModbusParser
from semana1.uart_driver.device import UartDevice

def test_device_conexion_y_desconexion():
    """Test 1: Verifica el control de los estados físicos de conexión[cite: 1]."""
    config = UartConfig(baudrate=9600)
    parser = ModbusParser()
    device = UartDevice(config, parser)
    
    assert device.is_connected is False
    device.connect()
    assert device.is_connected is True
    device.disconnect()
    assert device.is_connected is False

def test_device_read_and_parse_exitoso():
    """Test 2: Prueba la lectura exitosa mediante la inyección dinámica del parser[cite: 1]."""
    config = UartConfig(baudrate=115200)
    parser = ModbusParser()
    device = UartDevice(config, parser)
    
    device.connect()
    trama_modbus = b"\x01\x03\x00\x04"  # Frame válido para Modbus
    resultado = device.read_and_parse(trama_modbus)
    
    assert resultado["protocolo"] == "Modbus RTU"
    assert resultado["slave_id"] == 1

def test_device_error_si_no_esta_conectado():
    """Test 3: Debe lanzar RuntimeError si se intentan procesar bytes sin abrir el puerto[cite: 1]."""
    config = UartConfig(baudrate=9600)
    parser = ModbusParser()
    device = UartDevice(config, parser)
    
    # Intentar leer directo sin llamar a device.connect()
    with pytest.raises(RuntimeError) as exc_info:
        device.read_and_parse(b"\x01\x03\x00\x04")
    assert "no está conectado" in str(exc_info.value)