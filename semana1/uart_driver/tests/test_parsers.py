import pytest
from semana1.uart_driver.parsers import ModbusParser, NMEAParser

# =====================================================================
# TESTS: ModbusParser (3 Tests Obligatorios)[cite: 1]
# =====================================================================

def test_modbus_can_parse_valido():
    parser = ModbusParser()
    trama_valida = b"\x01\x03\x00\x01" # Slave ID 1, Función 3 (Read), Dirección 1
    assert parser.can_parse(trama_valida) is True

def test_modbus_rejects_nmea_or_short_frames():
    parser = ModbusParser()
    assert parser.can_parse(b"$GPGGA,1234") is False  # Es NMEA, no Modbus
    assert parser.can_parse(b"\x01\x02") is False       # Demasiado corta

def test_modbus_parse_exitoso():
    parser = ModbusParser()
    trama = b"\x05\x03\x02\xff\xff" # Slave ID 5
    resultado = parser.parse(trama)
    assert resultado["protocolo"] == "Modbus RTU"
    assert resultado["slave_id"] == 5
    assert resultado["function_code"] == 3


# =====================================================================
# TESTS: NMEAParser (3 Tests Obligatorios)[cite: 1]
# =====================================================================

def test_nmea_can_parse_valido():
    parser = NMEAParser()
    trama_gps = b"$GPGGA,123519,1924.000,N,09624.000,W"
    assert parser.can_parse(trama_gps) is True

def test_nmea_rejects_modbus_frames():
    parser = NMEAParser()
    trama_binaria = b"\x01\x03\x00\x02"
    assert parser.can_parse(trama_binaria) is False

def test_nmea_parse_exitoso_y_malformado():
    parser = NMEAParser()
    trama_gps = b"$GPGGA,201500,1926.123,N,09612.456,W"
    resultado = parser.parse(trama_gps)
    
    assert resultado["protocolo"] == "NMEA"
    assert resultado["latitud"] == "1926.123"
    assert resultado["longitud"] == "09612.456"

    # Caso malformado: Lanzar excepción si faltan campos indispensables
    with pytest.raises(ValueError):
        parser.parse(b"$GPGGA,corto")