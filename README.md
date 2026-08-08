# SensorHub API

API REST profesional para la ingesta de telemetría y gestión de sensores, desarrollada bajo principios de arquitectura limpia, contenerización y despliegue continuo.

![Build Status](https://github.com/Alexander-multiplexor/sdlc-electronica-Alexander/actions/workflows/ci.yml/badge.svg)

## 🚀 Despliegue en Producción
La aplicación se encuentra desplegada y viva en Render:
*   **Documentación API (Swagger UI):** [https://sensorhub-api-jds4.onrender.com/docs](https://sensorhub-api-jds4.onrender.com/docs)
*   **Health Check:** [https://sensorhub-api-jds4.onrender.com/health](https://sensorhub-api-jds4.onrender.com/health)

## 🛠️ Ejecución Local
Para levantar el entorno completo (API + PostgreSQL) con un solo comando:

```bash
docker compose up --build
```

🏗️ Stack Tecnológico
Backend: FastAPI

Base de Datos: PostgreSQL

Orquestación: Docker & Docker Compose

Pipeline: GitHub Actions (CI/CD)

Despliegue: Render (Infrastructure as Code)

🧪 Calidad de Código
El proyecto cuenta con un pipeline de integración continua que garantiza:

Linting: Ruff

Tipado: Mypy

Pruebas: Pytest con cobertura >80%