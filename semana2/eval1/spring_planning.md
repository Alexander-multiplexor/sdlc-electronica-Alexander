# Sprint 1 Planning — Monitoreo IoT Bodega

* **Sprint Goal:** Implementar el núcleo de procesamiento de lecturas IoT, detección de anomalías por umbrales configurables y despacho multicanal de alertas con cobertura $\ge 80\%$.
* **Historias Seleccionadas:** US-01, US-02, US-03, US-04, US-05 (Total: 18 Story Points).

## Desglose de Tareas ($\le 4\text{ h}$ cada una)
1. **[T-01]** Crear modelo `SensorReading` con validación de rangos (2 h).
2. **[T-02]** Implementar `AnomalyDetector` con inyección de umbrales via constructor (3 h).
3. **[T-03]** Diseñar interfaz abstracta `AlertStrategy` y estrategias `ConsoleAlert` / `FileAlert` (3 h).
4. **[T-04]** Crear `AlertManager` para coordinación multicanal (2 h).
5. **[T-05]** Integrar pruebas unitarias y verificar cobertura con `pytest-cov` (2 h).

## Definition of Done (DoD)
* [x] Criterios de aceptación Gherkin cumplidos y validados con tests automatizados.
* [x] Cobertura de pruebas $\ge 80\%$ en `src/`.
* [x] `ruff check .` sin advertencias ni errores.
* [x] `mypy src/` en modo estricto sin errores de tipado.
* [x] Commits en Git respetando la secuencia estricta TDD (RED $\rightarrow$ GREEN $\rightarrow$ REFACTOR).