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

## 👥 Ronda 2 de Peer Review: Humano vs. IA

Se realizó la revisión cruzada del Pull Request asignado aplicando la **Checklist de 10 Puntos de Arquitectura y Calidad**:

### Checklist de 10 Puntos
1. [x] **SRP:** ¿Cada clase y función tiene una responsabilidad única y delimitada?
2. [x] **DIP:** ¿La lógica de negocio depende de abstracciones (`Protocol`) en lugar de bases de datos concretas?
3. [x] **Manejo de Errores:** ¿Se manejan excepciones de dominio específicas sin silenciar errores con `except:` genéricos?
4. [x] **Tipado Estático:** ¿Todos los parámetros y retornos cuentan con type hints válidos para `mypy`?
5. [x] **Pureza Funcional:** ¿Las funciones de cálculo y conversión no mutan estado global?
6. [x] **Seguridad:** ¿Se previenen desbordamientos numéricos y datos no validados en endpoints?
7. [x] **Testabilidad:** ¿Existen pruebas unitarias para casos normales y casos límite (límites físicos, nulos, vacíos)?
8. [x] **Asincronía Segura:** ¿Se evita el bloqueo del Event Loop (`asyncio`)?
9. [x] **Nomenclatura:** ¿El vocabulario de variables y clases refleja con precisión el dominio de sensores y telemetría?
10. [x] **Monolito Modular:** ¿Se respeta el flujo de dependencias entre routers, services y repositories?

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