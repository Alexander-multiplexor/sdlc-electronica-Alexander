from dataclasses import FrozenInstanceError

import pytest

from semana1.uart_driver.config import UartConfig


def test_config_creacion_exitosa():
    """Test 1: Verifica que se cree correctamente con datos válidos."""
    config = UartConfig(baudrate=115200, parity="E", timeout=2.0)
    assert config.baudrate == 115200
    assert config.parity == "E"
    assert config.stop_bits == 1
    assert config.timeout == 2.0


def test_config_baudrate_invalido_lanza_excepcion():
    """Test 2: Debe lanzar ValueError si el baudrate no es estándar."""
    with pytest.raises(ValueError) as exc_info:
        UartConfig(baudrate=9999)  # Baudrate inexistente
    assert "no soportado" in str(exc_info.value)


def test_config_es_inmutable():
    """Test 3: Al ser frozen, modificar un atributo debe lanzar FrozenInstanceError."""
    config = UartConfig(baudrate=9600)
    with pytest.raises(FrozenInstanceError):
        config.baudrate = 115200  # Intento ilegal de modificación
