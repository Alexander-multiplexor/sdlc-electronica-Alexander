# Product Backlog — Sistema de Monitoreo IoT para Bodega Industrial

## Priorización y Estimación
* **Priorización:** Metodología MoSCoW (Must have, Should have, Could have, Won't have).
* **Estimación:** Serie de Fibonacci relative story points (1, 2, 3, 5, 8, 13).

---

### US-01: Registro y consulta de sensores en el sistema
**Prioridad:** Must Have | **Story Points:** 3  
**Como** operador de planta,  
**quiero** registrar la información técnica de los sensores y consultar su estado,  
**para** mantener un inventario activo y confiable de la infraestructura IoT de la bodega.

```gherkin
Scenario: Registrar un nuevo sensor correctamente
  Given que el sensor con ID "TEMP-01" no existe en el registro
  When el usuario registra el sensor "TEMP-01" con tipo "Temperatura" y ubicación "Nave A"
  Then el sistema guarda el sensor exitosamente con estado "ACTIVO"

Scenario: Rechazar consulta de sensor no existente
  Given que no existe ningún sensor registrado con ID "GHOST-99"
  When el operador solicita la información del sensor "GHOST-99"
  Then el sistema lanza un error de tipo "SensorNotFoundError"
```

### US-02: Lectura de temperatura y humedad con validación
**Prioridad:** Must Have | Story Points: 5
**Como** sistema de adquisición de datos,
**quiero** procesar las lecturas con timestamp de los sensores registrados,
**para** almacenar mediciones válidas y descartar datos corruptos.

```gherkin
Scenario: Almacenar lectura dentro del rango válido
  Given un sensor activo con ID "TEMP-01"
  When se recibe una lectura de 24.5 °C con timestamp actual
  Then la lectura es aceptada y agregada al historial del sensor "TEMP-01"

Scenario: Rechazar lectura fuera del rango físico de operación
  Given un sensor activo con ID "TEMP-01"
  When se recibe una lectura de 150.0 °C
  Then el sistema rechaza la lectura por superar el límite físico y genera un registro de advertencia
  ```
### US-03: Detección automatizada de anomalías
**Prioridad:** Must Have | Story Points: 5
**Como** supervisor de seguridad industrial,
**quiero** que el sistema detecte lecturas que superen umbrales críticos configurables,
**para** identificar situaciones de riesgo en la bodega a tiempo.

```gherkin
Scenario: Detectar temperatura excesiva superando el umbral
  Given un AnomalyDetector configurado con un umbral de temperatura de 35.0 °C
  When se evalúa una lectura de 36.2 °C del sensor "TEMP-01"
  Then el detector identifica la lectura como anomalía de tipo "CRITICAL_TEMP"
```