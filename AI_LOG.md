# AI_LOG.md · Bitácora de Desarrollo Asistido con IA (Semana 5)

**Curso:** De Electrónica a Desarrollo de Software con IA  
**Proyecto:** SensorHub API  
**Nivel alcanzado:** Alto Potencial  
**Regla de trabajo:** *"Trata el código de la IA como el PR de un colega junior brillante pero descuidado — nunca hagas merge de algo que no puedas explicar y defender tú mismo."*

---

## 📅 Entradas Semanales de Bitácora

### Entrada 1 · Martes 11/08/2026: Trazabilidad con Aider y Calibración ADC
* **Objetivo:** Implementar la función de calibración y conversión de hardware `raw_to_calibrated_voltage` en `semana5/conversions.py`.
* **Herramienta:** Aider CLI (`aider-chat` con `gemini-1.5-pro`).
* **Prompt utilizado:**
  > "CONTEXTO: SensorHub (Python 3.12). TAREA: Escribe una función pura `raw_to_calibrated_voltage` en `semana5/conversions.py`. RESTRICCIONES: Type hints estrictos, docstring Google style, validar resolución de bits levantando ValueError, redondeo a 4 decimales. ENTREGA: Solo la función."
* **Código generado por la IA:** La IA utilizó división entera `//` en el cálculo de voltaje, lo que truncaba los decimales a 0.
* **Intervención y Criterio Humano:** Modifiqué la fórmula a división flotante `/` y agregué validación explícita para evitar lecturas negativas provenientes de ruido en el ADC.
* **Trazabilidad Git:** El commit quedó registrado en el git log con la etiqueta oficial `Co-authored-by: aider <aider@aider.chat>`.

---

### Entrada 2 · Jueves 13/08/2026: Code Review Asistido y Refactor DIP
* **Objetivo:** Auditar `SensorService` identificando deuda técnica, violaciones SOLID y riesgos de asincronía.
* **Herramienta:** Copilot Chat / Gemini.
* **Hallazgos clave analizados:**
  1. *Aceptado:* Detección de acoplamiento directo a base de datos. Se extrajo `ReadingRepositoryInterface` con `typing.Protocol` (DIP).
  2. *Aceptado:* Reemplazo de `time.sleep` por `asyncio.sleep` para evitar congelar el Event Loop.
  3. *Rechazado:* Sugerencia de la IA de meter RabbitMQ/Kafka. Se descartó por sobreingeniería (*MonolithFirst*).
  4. *Rechazado:* Alucinación de supuesta inyección SQL en SQLAlchemy 2.0. Se comprobó que el ORM compila queries parametrizadas de forma segura.
* **Pipeline:** Se añadieron 5 tests unitarios con un `FakeReadingRepository` en memoria, alcanzando 30 tests en verde.

---

### Entrada 3 · Viernes 14/08/2026: Feature de Detección de Anomalías (TDD + OCP)
* **Objetivo:** Desarrollar el motor de evaluación de umbrales con estrategias de alerta intercambiables.
* **Herramienta:** Copilot Chat.
* **Iteración TDD:**
  1. **Red:** Se escribieron pruebas unitarias para `LogAlertStrategy` y `WebhookAlertStrategy` antes de implementar la lógica.
  2. **Green:** Se implementó `AnomalyDetectionService` y el contrato `AlertNotificationStrategy` (`typing.Protocol`).
  3. **Refactor:** Se protegió la ejecución de las estrategias dentro de un bloque `try/except` para que la falla de un canal de notificación no interrumpa el pipeline de ingesta.
* **Resultado:** 35 tests pasando con 94.51% de cobertura global.

---

### 🔍 Peer Review Ronda 2 — Evaluación del PR de Alberto Hernández (@AlbertohdzL)

* **Repositorio auditado:** `sdlc-electronica-alberto-hernandez`
* **Fecha:** 15 de agosto de 2026

#### 1. Resumen de la Revisión con Checklist de 10 Puntos
* **Fortalezas:**
  * **OCP ejemplar:** La implementación del patrón Strategy en `AnomalyDetector` (`AlertStrategy` con `InMemoryAlertStrategy` y `ConsoleAlertStrategy`) desacopla totalmente la regla de negocio del canal de alerta.
  * **Validación de física real:** Las conversiones en `conversions.py` protegen contra lecturas por debajo del cero absoluto ($-273.15\text{ }^\circ\text{C}$ / $-459.67\text{ }^\circ\text{F}$) mediante `ValueError`.
  * **Buenas prácticas de testing:** Pruebas limpias usando `capsys` para validar salidas de terminal y `MagicMock` para verificar llamadas a contratos abstractos.

* **Oportunidades de Mejora (Deuda Técnica detectada):**
  * **DIP / SRP en `SensorService`:** Se recomienda desacoplar `HTTPException` del servicio creando excepciones de dominio (`SensorNotFoundError`, `SensorAlreadyExistsError`) para que el router las capture.
  * **Sanitización y Paginación:** Acotar `limit = min(limit, 100)` para evitar cargas masivas de memoria y aplicar `.strip()` a los identificadores.

#### 2. Conclusiones Clave de la Dinámica Humano vs. IA

1. **La IA detecta riesgos de concurrencia sutiles:** La IA identificó la condición de carrera TOCTOU (*Time-of-Check to Time-of-Use*) en la creación de sensores, un detalle de infraestructura que el ojo humano suele pasar por alto al enfocarse en la lógica de negocio.
2. **El humano evalúa el diseño arquitectónico integral:** Mientras la IA evalúa línea por línea, el criterio humano validó que el patrón Strategy cumpliera con los principios de diseño de software mantenible (OCP/DIP) y no agregara complejidad innecesaria.
3. **Sinergia para un Code Review profesional:** El checklist estructurado permitió que la auditoría no fuera una simple corrección de estilo, sino un análisis profundo de resiliencia, seguridad y arquitectura limpia.

---

### Cuadro Comparativo de Hallazgos

| Dimensión | Revisor Humano | Revisor IA |
|---|---|---|
| **Lógica de Dominio y Hardware** | Detectó que la calibración asumía un ADC de 10 bits ($1023$) cuando el sensor físico opera a 12 bits ($4095$). | No identificó la discrepancia física; asumió la fórmula matemática como válida. |
| **Resiliencia de Red** | Notó que las peticiones HTTP externas no definían `timeout`, con riesgo de colgar workers. | Sugirió añadir validación de formato con expresiones regulares complejas. |
| **Simplicidad vs Sobreingeniería** | Priorizó mantener la solución simple (KISS / YAGNI) dentro del monolito existente. | Propuso introducir una cola de mensajería distribuida y microservicios prematuros. |

---

### 💡 3 Conclusiones Clave de la Comparativa

1. **La IA revisa sintaxis; el humano audita el dominio físico:** La IA valida tipado y formato de comentarios, pero carece de intuición sobre el comportamiento del hardware (resolución de convertidores ADC, voltajes de referencia y rangos de operación reales).
2. **Filtro contra la sobreingeniería (*Architecture Gatekeeper*):** Los LLMs tienen sesgo hacia patrones complejos y arquitecturas distribuidas innecesarias. El rol crítico del desarrollador es rechazar sugerencias que aumenten la deuda técnica u operativa.
3. **El prompt determina el rigor del Code Review:** Prompts genéricos producen revisiones superficiales; prompts con restricciones y checklist estructuradas logran auditorías equivalentes a un ingeniero senior.

---

## 📚 Notas para la Discusión: Martin Fowler (*Microservices* & *MonolithFirst*)

### ¿Cuándo **NO** usar microservicios?

1. **Equipos pequeños y proyectos en fase temprana:** La sobrecarga operativa de gestionar despliegues independientes, observabilidad distribuida (OpenTelemetry, tracing) y monitoreo supera ampliamente el beneficio de separación.
2. **Límites de Dominio Difusos (*Unclear Bounded Contexts*):** Cuando el modelo de negocio cambia con rapidez, dividir en microservicios obliga a realizar refactors inter-servicio costosos y despliegues acoplados.
3. **Sistemas con requerimientos de baja latencia:** En ingesta de telemetría de sensores en tiempo real, las llamadas de red entre microservicios añaden latencia y puntos de falla innecesarios frente a llamadas en memoria bien estructuradas.
4. **Conclusión para SensorHub:** Un **Monolito Modular** con inversión de dependencias (`Protocol`) ofrece modularidad, alta velocidad de pruebas unitarias y simplicidad operativa sin pagar el costo de infraestructura distribuida.