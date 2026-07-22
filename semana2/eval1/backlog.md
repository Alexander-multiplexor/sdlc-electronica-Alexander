# Product Backlog — Sistema de Monitoreo IoT para Bodega Industrial

## US-01: Validar e instanciar lecturas de sensores (SensorReading)
**Como** operador de la bodega industrial,  
**quiero** que el sistema valide que las lecturas de temperatura y humedad estén dentro de rangos físicamente posibles,  
**para** evitar procesar datos corruptos procedentes del hardware.  
* **Prioridad MoSCoW:** Must Have  
* **Story Points:** 3  

```gherkin
Scenario: Lectura válida dentro de rangos operativos
  Given un sensor con id "TEMP-01"
  When se registra una temperatura de 24.5 °C y humedad de 50.0%
  Then la lectura se crea exitosamente con estado "OK"

Scenario: Rechazar temperatura fuera de límite físico
  Given un sensor con id "TEMP-02"
  When se registra una temperatura de 150.0 °C
  Then el sistema lanza un ValueError indicando temperatura fuera de rango
```

## US-02: Detección de anomalías térmicas e hídricas con umbrales inyectados (AnomalyDetector)
**Como** supervisor de seguridad industrial,
**quiero** detectar anomalías cuando la temperatura supere los 35 °C o la humedad supere el 80%,
**para** reaccionar antes de que los productos almacenados se dañen.
* **Prioridad MoSCoW:** Must Have
* **Story Points:** 5

```gherkin
Scenario: Detectar anomalía por alta temperatura
  Given un detector configurado con umbrales de 35.0 °C y 80.0%
  When recibe una lectura con temperatura de 36.5 °C y humedad del 50.0%
  Then evalúa la lectura como anomalía por "TEMPERATURA_ALTA"

Scenario: Operación dentro de límites normales
  Given un detector configurado con umbrales de 35.0 °C y 80.0%
  When recibe una lectura con temperatura de 22.0 °C y humedad del 45.0%
  Then evalúa la lectura como "NORMAL"
```

## US-03: Despacho multicanal de alertas (AlertManager)
**Como** encargado de mantenimiento,
**quiero** que las anomalías detectadas se envíen simultáneamente a consola y a un archivo de registro,
**para** tener visibilidad inmediata y un histórico ejecutable.
* **Prioridad MoSCoW:** Must Have
* **Story Points:** 5

```gherkin
Scenario: Emitir alerta a múltiples canales activos
  Given un AlertManager con estrategias "ConsoleAlert" y "FileAlert" registradas
  When se notifica una anomalía "TEMPERATURA_ALTA en TEMP-01"
  Then el mensaje se imprime en consola y se escribe en el archivo de log
```

## US-04: Persistencia de lecturas en formato JSON-lines
**MoSCoW:** Should Have | Story Points: 3

```gherkin: Al recibir una lectura válida, el sistema la apenda como una nueva línea JSON en readings.jsonl.
```

## US-05: Configuración dinámica de umbrales sin reiniciar
**MoSCoW:** Should Have | Story Points: 2

```gherkin: Al actualizar los umbrales del detector en tiempo de ejecución, las lecturas subsecuentes se evalúan contra los nuevos valores.
```

## US-06: Simulación de lote de 10 sensores con distribución gaussiana
**MoSCoW:** Could Have | Story Points: 8

```gherkin: El generador emite tramas para 10 sensores durante 60 ciclos con variaciones estocásticas gaussianas.
```

## US-07: Verificación de estado de salud de sensores (Heartbeat)
**MoSCoW:** Should Have | Story Points: 3

```gherkin: Si un sensor no envía lecturas por más de 60 segundos, se marca como "INACTIVO".
```

## US-08: Filtrado de picos de ruido por hardware
**MoSCoW:** Could Have | Story Points: 5

```gherkin: Si una lectura cambia más de 20 °C en 30 segundos respecto a la anterior, se marca como "RUIDO" y se ignora.
```

## US-09: Generación de reporte diario de anomalías
**MoSCoW:** Won't Have (este Sprint) | Story Points: 5

## US-10: Dashboard gráfico web de monitoreo en tiempo real
**MoSCoW:** Won't Have (este Sprint) | Story Points: 13