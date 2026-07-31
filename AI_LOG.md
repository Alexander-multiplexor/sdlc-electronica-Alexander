# Bitácora de Uso Reflexivo de IA (AI_LOG.md)

## Semana 3 — Arquitectura en Capas, APIs REST y Persistencia

### Entrada 1: Validación Física en Esquemas Pydantic y Tipado Estático Mypy
* **Fecha**: 30 de julio de 2026
* **Herramienta**: Copilot / Gemini
* **Prompt**:
  > "Genera un modelo Pydantic `ReadingCreate` que valide unidades de medida y límites físicos reales por tipo de sensor (TEMPERATURE, HUMIDITY, PRESSURE) utilizando un diccionario de reglas."

* **Propuesta de la IA**:
  La IA generó el validador `@model_validator` utilizando un diccionario estático `PHYSICAL_LIMITS` con reglas por tipo de sensor, pero sin anotaciones de tipos explícitas para las claves internas.

* **Decisión**: **Modificar**
  * **Por qué**: Al ejecutar `mypy app/`, el analizador estático infirió el tipo de las reglas internas como `dict[str, object]`, lanzando 4 errores del tipo `Unsupported operand types` e `Unsupported right operand type for in ("object")`.
  * **Cambio aplicado**: Se definió un `TypedDict` llamado `SensorPhysicsRule` especificando `valid_units: set[str]`, `min_val: float` y `max_val: float`. Con esto se mantuvo la validación de física real requerida por el dominio y se logró un chequeo de tipos estático completamente limpio (`Success: no issues found`).

---

### Entrada 2: Implementación de Repositorio con SQLAlchemy 2.0 vs Sintaxis Legacy 1.x
* **Fecha**: 30 de julio de 2026
* **Herramienta**: Copilot / Gemini
* **Prompt**:
  > "Escribe la función `list_by_sensor` en `ReadingRepository` para consultar lecturas de la base de datos con paginación (`limit`, `offset`) y filtros opcionales por rango de fecha (`from_date`, `to_date`)."

* **Propuesta de la IA**:
  La IA sugirió utilizar la sintaxis legacy de SQLAlchemy 1.x basada en `db.query(ReadingModel).filter(...)`.

* **Decisión**: **Rechazar / Reescritura**
  * **Por qué**: El stack oficial del programa exige SQLAlchemy 2.0 tipado. La sintaxis `db.query()` está en desuso y no aprovecha la inferencia de tipos con `Mapped[...]` requerida por `mypy`.
  * **Cambio aplicado**: Se reescribió el repositorio utilizando la API de consulta de SQLAlchemy 2.0 (`select(ReadingModel).where(...)`), encadenando condicionalmente los filtros temporales y ordenando por `created_at.desc()`. Además, se anotó el retorno como `Sequence[ReadingModel]` para cumplir con los estándares de diseño del patrón repositorio.

---

### Entrada 3: Configuración del Fixture de Base de Datos para Tests de Integración
* **Fecha**: 30 de julio de 2026
* **Herramienta**: Copilot / Gemini
* **Prompt**:
  > "Crea un fixture en `tests/conftest.py` para levantar una base de datos SQLite en memoria (`sqlite:///:memory:`) y probar la API con `TestClient` de FastAPI."

* **Propuesta de la IA**:
  La IA propuso una configuración básica con `create_engine("sqlite:///:memory:")` sin registrar los modelos en los metadatos ni especificar el pool de conexiones.

* **Decisión**: **Modificar**
  * **Por qué**: Al ejecutar `pytest`, los tests fallaban con `sqlite3.OperationalError: no such table: sensors`. En SQLite en memoria, cada nueva conexión o hilo abre una base de datos aislada e independiente, lo que provocaba que la aplicación de FastAPI no encontrara las tablas creadas durante el setup de la prueba.
  * **Cambio aplicado**: Se agregó la importación explícita de `app.models.sensor_hub` para registrar las tablas en `Base.metadata`, y se configuró `poolclass=StaticPool` en el `create_engine`. Esta modificación permitió que la sesión de prueba y la app de FastAPI compartieran la misma instancia en memoria, logrando que los 13 tests pasen en verde con un 95.85% de cobertura.