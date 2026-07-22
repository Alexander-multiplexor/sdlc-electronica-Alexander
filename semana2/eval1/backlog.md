# Product Backlog — Sistema de Monitoreo IoT para Bodega Industrial

## US-01: Validar e instanciar lecturas de sensores (SensorReading)
**Como** operador de la bodega industrial,  
**quiero** que el sistema valide que las lecturas de temperatura y humedad estén dentro de rangos físicamente posibles,  
**para** evitar procesar datos corruptos procedentes del hardware.  
* **Prioridad MoSCoW:** Must Have  
* **Story Points:** 3  

```gherkin
Escenario: Lectura válida dentro de rangos operativos
  Given un sensor con id "TEMP-01"
  When se registra una temperatura de 24.5 °C y humedad de 50.0%
  Then la lectura se crea exitosamente con estado "OK"

Escenario: Rechazar temperatura fuera de límite físico
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
Escenario: Detectar anomalía por alta temperatura
  Given un detector configurado con umbrales de 35.0 °C y 80.0%
  When recibe una lectura con temperatura de 36.5 °C y humedad del 50.0%
  Then evalúa la lectura como anomalía por "TEMPERATURA_ALTA"

Escenario: Operación dentro de límites normales
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
Escenario: Emitir alerta a múltiples canales activos
  Given un AlertManager con estrategias "ConsoleAlert" y "FileAlert" registradas
  When se notifica una anomalía "TEMPERATURA_ALTA en TEMP-01"
  Then el mensaje se imprime en consola y se escribe en el archivo de log
```

## US-04: Persistencia de lecturas en formato JSON-lines
**MoSCoW:** Should Have | **Story Points:** 3

```gherkin:
Escenario: Guardar lectura válida en archivo JSONL
  Dado un archivo de registro "readings.jsonl"
  Cuando el sistema recibe una lectura válida del sensor "TEMP-01"
  Entonces apenda una nueva línea en formato JSON con la lectura y timestamp actual
```

## US-05: Configuración dinámica de umbrales sin reiniciar
**MoSCoW:** Should Have | **Story Points:** 2

```gherkin
Escenario: Actualizar umbral de temperatura en tiempo de ejecución
  Dado un AnomalyDetector configurado inicialmente a 35.0 °C
  Cuando se actualiza el umbral máximo de temperatura a 30.0 °C
  Entonces una lectura posterior de 32.0 °C es evaluada como "TEMPERATURA_ALTA"
```

## US-06: Simulación de lote de 10 sensores con distribución gaussiana
**MoSCoW:** Could Have | **Story Points:** 8

```gherkin
Escenario: Generar ciclo completo para flota de sensores
  Dado un SensorSimulator configurado con 10 sensores
  Cuando se solicita la generación de un ciclo de monitoreo
  Entonces devuelve una lista de 10 objetos SensorReading con valores estocásticos gaussianos
```

## US-07: Verificación de estado de salud de sensores (Heartbeat)
**MoSCoW:** Should Have | **Story Points:** 3

```gherkin
Escenario: Marcar sensor como inactivo por falta de reporte
  Dado un sensor "TEMP-01" cuya última lectura fue hace 65 segundos
  Cuando el monitor de salud ejecuta la verificación
  Entonces el estado del sensor "TEMP-01" cambia a "INACTIVO"
```

## US-08: Filtrado de picos de ruido por hardware
**MoSCoW:** Could Have | **Story Points:** 5

```gherkin
Escenario: Descartar lectura por cambio térmico abrupto
  Dado que la última lectura del sensor "TEMP-01" fue de 20.0 °C
  Cuando recibe una nueva lectura de 45.0 °C enviada 10 segundos después
  Entonces la lectura es marcada como "RUIDO" y no se envía a procesamiento
```

## US-09: Generación de reporte diario de anomalías
**Como** gerente de operaciones de la bodega,  
**quiero** recibir un reporte diario consolidado con el resumen de todas las anomalías detectadas en las últimas 24 horas,  
**para** evaluar el desempeño térmico de las instalaciones y tomar decisiones preventivas.  
* **Prioridad MoSCoW:** Won't Have (este Sprint)  
* **Story Points:** 5  

```gherkin
Escenario: Generar reporte diario con anomalías acumuladas
  Dado un historial de lecturas registradas durante las últimas 24 horas con 3 anomalías
  Cuando el sistema ejecuta el proceso batch de medianoche
  Entonces genera un archivo de reporte con el conteo de incidencias agrupadas por sensor

Escenario: Generar reporte en un día sin incidencias
  Dado que en las últimas 24 horas no se registró ninguna anomalía
  Cuando se ejecuta la generación del reporte diario
  Entonces el reporte se crea indicando el estado "Sin incidencias registradas"
```

## US-10: Dashboard gráfico web de monitoreo en tiempo real
**Como** operador de planta,  
**quiero** visualizar en una interfaz web los valores de los 10 sensores con gráficas en tiempo real,  
**para** monitorear visualmente la bodega sin necesidad de consultar archivos de texto o consola.  
* **Prioridad MoSCoW:** Won't Have (este Sprint)  
* **Story Points:** 13  

```gherkin
Escenario: Actualización en tiempo real de indicadores
  Dado que el operador tiene abierto el Dashboard web en su navegador
  Cuando el sensor "TEMP-01" envía una nueva lectura de 24.5 °C
  Then la tarjeta del sensor "TEMP-01" en la pantalla actualiza su valor en menos de 1 segundo

Escenario: Alerta visual por anomalía detectada
  Dado un sensor "TEMP-02" que registra una temperatura de 37.0 °C (anomalía)
  Cuando la lectura llega al Dashboard web
  Entonces la tarjeta del sensor "TEMP-02" cambia su indicador a color rojo y emite un aviso visual
```