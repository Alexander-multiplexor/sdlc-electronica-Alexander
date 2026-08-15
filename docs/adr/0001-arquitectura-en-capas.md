# ADR 0001: Arquitectura en Capas y Monolito Modular para SensorHub

## Estado
Aceptado

## Fecha
2026-08-14

## Contexto
El sistema **SensorHub** gestiona la ingesta, calibración y persistencia de telemetría proveniente de sensores físicos e industriales. 

En iteraciones tempranas, la lógica de negocio se encontraba estrechamente acoplada a los endpoints de FastAPI y a consultas directas de base de datos. Este acoplamiento generaba los siguientes problemas:
1. **Dificultad en pruebas unitarias:** No era posible testear la calibración y reglas de negocio sin depender de una base de datos real SQLite/PostgreSQL.
2. **Fragilidad ante cambios de infraestructura:** Cambiar de base de datos o reemplazar el transporte HTTP por MQTT o WebSockets requería modificar la lógica de dominio.
3. **Mantenibilidad:** El código mezclaba validaciones HTTP, lógica física y serialización en un solo lugar.

---

## Decisión
Adoptamos una **Arquitectura en Capas (Layered Architecture)** organizada en un **Monolito Modular**, compuesta por:

```text
Routers (FastAPI / HTTP)
       │
       ▼
Services (Lógica de Dominio y Calibración)
       │
       ▼  [Abstracción vía Protocols - DIP]
Repositories (Persistencia SQLite / PostgreSQL)
       │
       ▼
Models & Schemas (Entidades de Dominio y Validación Pydantic)
```

## Reglas de Diseño:
- Principio de Inversión de Dependencias (DIP): La capa de servicios nunca depende de implementaciones concretas de base de datos, sino de abstracciones definidas mediante typing.Protocol (e.g. ReadingRepositoryInterface).

- Monolito Modular vs. Microservicios: De acuerdo con los principios de Martin Fowler (MonolithFirst), mantenemos el sistema como un solo proceso desplegable con límites modulares claros, evitando la complejidad innecesaria de red, latencia y consistencia distribuida.

## Consecuencias
### Positivas (+)
- Testabilidad Determinista y Rápida: Es posible ejecutar tests unitarios de servicios en milisegundos mediante repositorios en memoria (FakeReadingRepository) sin realizar I/O real.

- Desacoplamiento de Persistencia: Migrar de SQLite a TimescaleDB o PostgreSQL solo requiere implementar un nuevo adaptador de repositorio sin tocar la lógica de negocio.

- Separación de Responsabilidades: Cada capa posee un propósito único y bien delimitado (SRP).

### Negativas (-)
- Ceremonia Inicial: Incremento en la cantidad de archivos, protocolos e inyecciones necesarias para operaciones simples.

- Mapeo de Datos: Necesidad de convertir modelos de ORM a entidades de dominio y esquemas Pydantic.