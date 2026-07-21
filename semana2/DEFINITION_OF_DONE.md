# Definition of Done (DoD) — Semana 2

Para considerar que una historia de usuario o incremento está **completado (Done)**, debe cumplir con la siguiente lista de verificación innegociable:

1. **Criterios de Aceptación:**
   - Todos los escenarios planteados en formato Gherkin están implementados y verificados.

2. **Calidad de Pruebas (TDD):**
   - El historial de Git evidencia el ciclo *Red -> Green -> Refactor* (commit de tests previo al código).
   - Cobertura de código garantizada **≥ 80%**.

3. **Análisis Estático y Tipado:**
   - `ruff check .` se ejecuta sin advertencias ni errores.
   - `mypy .` aprueba el análisis estático de tipos sin fallos (`disallow_untyped_defs = true`).

4. **Revisión de Código (Workflow):**
   - El código fue integrado mediante un Pull Request (PR) desde una rama de característica (`feature/US-xx`).
   - El desarrollador leyó su propio `diff` completo antes de realizar el merge a `main`.

5. **Documentación y Bitácora:**
   - Documentación de funciones/clases actualizada con docstrings.
   - Entrada correspondiente añadida en `AI_LOG.md`.