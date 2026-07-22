# Bitácora de Uso de IA — Semana 2

## Entrada 1 — Estructura de Gherkin para Casos Borde
* **Promot:** "¿Cómo redactar un escenario Gherkin para rechazar datos corruptos en sensores de temperatura?"
* **Propuesta de IA:** Sugirió un escenario genérico sin tipos numéricos.
* **Decisión:** RECHAZADA y AJUSTADA. Se especificaron rangos numéricos explícitos (-50 °C a 100 °C) para garantizar que la prueba unitaria fuera directamente traducible a assertions de Python.

## Entrada 2 — Inyección de Dependencias vs Singleton en Detector
* **Prompt:** "¿Es conveniente implementar el AnomalyDetector como Singleton o pasar los umbrales por constructor?"
* **Propuesta de IA:** Sugirió usar un objeto global con constantes HARDCODED.
* **Decisión:** RECHAZADA. Se optó por inyectar `max_temp` y `max_humidity` en el `__init__` para cumplir con el principio OCP/DIP de SOLID y permitir tests aislados con distintos umbrales.

## Entrada 3 — Estrategia de Notificación de Alertas
* **Prompt:** "Propón una estructura en Python para notificar alertas a consola y archivo de texto."
* **Propuesta de IA:** Diseñó clases independientes con nombres heterogéneos sin interfaz común.
* **Decisión:** ACEPTADA PARCIALMENTE. Se refactorizó aplicando la clase base abstracta `AlertStrategy` (ABC) para permitir polimorfismo y extensibilidad en `AlertManager`.