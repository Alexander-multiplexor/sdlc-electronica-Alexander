from collections.abc import Sequence
from datetime import datetime

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.db import get_db
from app.schemas.reading import ReadingCreate, ReadingResponse
from app.services.reading_service import ReadingService

router = APIRouter(prefix="/sensors", tags=["Readings"])


def get_reading_service() -> ReadingService:
    return ReadingService()


@router.post(
    "/{sensor_id}/readings",
    response_model=ReadingResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Registrar una nueva lectura de telemetría",
)
def create_reading(
    sensor_id: str,
    reading_in: ReadingCreate,
    db: Session = Depends(get_db),
    service: ReadingService = Depends(get_reading_service),
) -> ReadingResponse:
    """
    Registra una lectura verificando:
    1. Que el sensor_id de la URL coincida con la lectura.
    2. Que la unidad y rango respeten la física real.
    3. Que el sensor esté registrado y activo.
    """
    # Garantiza coherencia entre URL y Body
    reading_in.sensor_id = sensor_id
    return service.record_reading(db, reading_in)  # type: ignore[return-value]


@router.get(
    "/{sensor_id}/readings",
    response_model=list[ReadingResponse],
    status_code=status.HTTP_200_OK,
    summary="Consultar historial de lecturas con paginación y filtro de fecha",
)
def list_readings_for_sensor(
    sensor_id: str,
    limit: int = Query(50, ge=1, le=100, description="Límite por página"),
    offset: int = Query(0, ge=0, description="Desplazamiento para paginación"),
    from_date: datetime | None = Query(
        None, description="Fecha inicial ISO (ej. 2026-07-01T00:00:00)"
    ),
    to_date: datetime | None = Query(
        None, description="Fecha final ISO (ej. 2026-07-31T23:59:59)"
    ),
    db: Session = Depends(get_db),
    service: ReadingService = Depends(get_reading_service),
) -> Sequence[ReadingResponse]:
    """Obtiene lecturas ordenadas cronológicamente con soporte de filtros temporales."""
    return service.list_readings_for_sensor(
        db,
        sensor_id=sensor_id,
        limit=limit,
        offset=offset,
        from_date=from_date,
        to_date=to_date,
    )  # type: ignore[return-value]