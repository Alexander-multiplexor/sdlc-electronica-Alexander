# Diagrama C4 — Nivel 2: Contenedores (Sistema de Monitoreo IoT)

```mermaid
graph TD
    User[Operador / Supervisor de Bodega]

    subgraph Sistema IoT [Sistema de Monitoreo IoT - Bodega Industrial]
        Sim[SensorSimulator\n Generador Gaussiano Flota 10 Sensores]
        Reading[SensorReading\n Validaciones de Rango Físico]
        Detector[AnomalyDetector\n Evaluador de Umbrales Configurable]
        AlertMgr[AlertManager\n Despachador Multicanal de Alertas]
    end

    subgraph Salidas [Canales de Notificación]
        Console[ConsoleAlertStrategy\n Salida Estándar STDOUT]
        FileLog[FileAlertStrategy\n Log File: integration_alerts.log]
    end

    User -->|Consulta logs y consola| Salidas
    Sim -->|Paso de lecturas cada 30s| Reading
    Reading -->|Trama validada| Detector
    Detector -->|Notifica si is_anomaly=True| AlertMgr
    AlertMgr -->|Estrategia 1| Console
    AlertMgr -->|Estrategia 2| FileLog