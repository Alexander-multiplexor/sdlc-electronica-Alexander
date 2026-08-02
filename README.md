# sdlc-electronica-Alexander
Este es mi repositorio público

1. **`sensors.sensor_id` (`index=True`)**:
   * *Por qué*: Las operaciones CRUD y las búsquedas por ID de sensor (`GET /sensors/{sensor_id}`) son las más comunes. Un índice B-Tree reduce la complejidad de búsqueda de $O(N)$ (escaneo completo) a $O(\log N)$.
2. **`readings.sensor_id` (`index=True`)**:
   * *Por qué*: Al consultar lecturas históricas por sensor (`GET /sensors/{sensor_id}/readings`), SQL realiza un filtrado por esta columna. Sin índice, la base de datos tendría que examinar millones de lecturas registradas globalmente.
3. **`readings.created_at` (`index=True`)**:
   * *Por qué*: El requerimiento exige **filtrar por rango de fechas** (`?from=...&to=...`) y paginar de manera cronológica. Indexar la estampa de tiempo permite a la BD realizar ordenamientos y búsquedas por rango de manera eficiente.
