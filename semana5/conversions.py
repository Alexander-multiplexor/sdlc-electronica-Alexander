"""Módulo de conversiones de ingeniería y calibración para SensorHub."""


def raw_to_calibrated_voltage(
    raw_value: int,
    v_ref: float = 3.3,
    adc_bits: int = 12,
    gain: float = 1.0,
    offset: float = 0.0,
) -> float:
    """Convierte una lectura digital ADC a voltaje calibrado.

    Args:
        raw_value: Valor entero del convertidor analógico-digital.
        v_ref: Voltaje de referencia del ADC en voltios.
        adc_bits: Resolución en bits del convertidor ADC.
        gain: Factor de escala lineal (ganancia de calibración).
        offset: Desplazamiento lineal en voltios.

    Returns:
        float: Voltaje calculado y calibrado redondeado a 4 decimales.

    Raises:
        ValueError: Si raw_value es negativo o supera el rango de resolución.
    """
    max_raw = (1 << adc_bits) - 1
    if not (0 <= raw_value <= max_raw):
        raise ValueError(f"raw_value ({raw_value}) fuera de rango para resolución de {adc_bits} bits [0, {max_raw}].")

    voltage_ideal = (raw_value / max_raw) * v_ref
    voltage_calibrated = (voltage_ideal * gain) + offset
    return round(voltage_calibrated, 4)


def celsius_to_fahrenheit(c: float) -> float:
    """Convierte temperatura de grados Celsius a Fahrenheit.

    Args:
        c: Temperatura en grados Celsius.

    Returns:
        float: Temperatura equivalente en Fahrenheit redondeada a 2 decimales.
    """
    f = (c * 9.0 / 5.0) + 32.0
    return round(f, 2)
