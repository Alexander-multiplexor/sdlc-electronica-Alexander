from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from app.db import Base, engine
from app.routers.reading_router import router as reading_router
from app.routers.sensor_router import router as sensor_router
from app.services.exceptions import (
    SensorAlreadyExistsError,
    SensorInactiveError,
    SensorNotFoundError,
    SensorTypeMismatchError,
)

# Crear tablas automáticamente al iniciar (en semana 4 usaremos Alembic)
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="SensorHub API",
    description="API REST profesional para ingesta de telemetría y gestión de sensores.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)


# --- MANEJADORES GLOBALES DE EXCEPCIONES DE DOMINIO (HTTP 400, 404, 409) ---


@app.exception_handler(SensorNotFoundError)
def sensor_not_found_handler(request: Request, exc: SensorNotFoundError) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"detail": str(exc)},
    )


@app.exception_handler(SensorAlreadyExistsError)
def sensor_already_exists_handler(request: Request, exc: SensorAlreadyExistsError) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={"detail": str(exc)},
    )


@app.exception_handler(SensorInactiveError)
def sensor_inactive_handler(request: Request, exc: SensorInactiveError) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": str(exc)},
    )


@app.exception_handler(SensorTypeMismatchError)
def sensor_type_mismatch_handler(request: Request, exc: SensorTypeMismatchError) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": str(exc)},
    )


# --- REGISTRO DE ROUTERS ---

app.include_router(sensor_router)
app.include_router(reading_router)


@app.get("/health", tags=["Health"], summary="Verificar estado de la API")
def health() -> dict[str, str]:
    return {"status": "ok"}
