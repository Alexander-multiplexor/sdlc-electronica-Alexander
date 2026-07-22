# Sprint 1 Retrospective — "Del Caos al Proceso"

## 1. Qué salió bien
* La adopción de TDD permitió detectar errores de validaciones antes de escribir lógica de negocio.
* La separación de responsabilidades (SOLID) facilitó probar las alertas mediante archivos temporales sin afectar el entorno local.

## 2. Qué se debe mejorar
* Estimar tareas con mayor holgura cuando involucran configuración de entorno (`pyproject.toml`, rutas de Python).

## 3. Acción Concreta de Mejora (Aceptada por el equipo)
* Integrar un script de verificación previo a los commits que ejecute `ruff check` y `pytest` de forma automatizada.