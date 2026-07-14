from hola_sensor import Sensor

def test_read_devuelve_valor_correcto():
    # 1. Preparar (Arrange): Instanciar la clase Sensor
    mi_sensor = Sensor()
    
    # 2. Actuar (Act): Llamar al método read()
    resultado = mi_sensor.read()
    
    # 3. Afirmar (Assert): Verificar que el resultado sea 23.5
    assert resultado == 23.5