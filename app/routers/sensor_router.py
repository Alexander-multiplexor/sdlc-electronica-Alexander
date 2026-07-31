from collections.abc import Sequence

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.db import get_db
from app.schemas.sensor import SensorCreate, SensorResponse, SensorUpdate
from app.services.sensor_service import SensorService

router = APIRouter(prefix="/sensors", tags=["Sensors"])


def get_sensor_service() -> SensorService:
    return SensorService()


@router.post(
    "",
    response_model=SensorResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Registrar un nuevo sensor",
)
def create_sensor(
    sensor_in: SensorCreate,
    db: Session = Depends(get_db),
    service: SensorService = Depends(get_sensor_service),
) -> SensorResponse:
    """Registra un nuevo dispositivo en el sistema. Lanza 409 si el sensor_id ya existe."""
    return service.create_sensor(db, sensor_in)  # type: ignore[return-value]


@router.get(
    "",
    response_model=list[SensorResponse],
    status_code=status.HTTP_200_OK,
    summary="Listar todos los sensores con paginación",
)
def list_sensors(
    limit: int = Query(50, ge=1, le=100, description="Límite de registros por página"),
    offset: int = Query(0, ge=0, description="Desplazamiento para paginación"),
    db: Session = Depends(get_db),
    service: SensorService = Depends(get_sensor_service),
) -> Sequence[SensorResponse]:
    """Obtiene el catálogo de sensores con soporte de limit y offset."""
    return service.list_sensors(db, limit=limit, offset=offset)  # type: ignore[return-value]


@router.get(
    "/{sensor_id}",
    response_model=SensorResponse,
    status_code=status.HTTP_200_OK,
    summary="Obtener detalle de un sensor",
)
def get_sensor(
    sensor_id: str,
    db: Session = Depends(get_db),
    service: SensorService = Depends(get_sensor_service),
) -> SensorResponse:
    """Busca un sensor por su ID único. Lanza 404 si no existe."""
    return service.get_sensor(db, sensor_id)  # type: ignore[return-value]


@router.patch(
    "/{sensor_id}",
    response_model=SensorResponse,
    status_code=status.HTTP_200_OK,
    summary="Actualizar parcialmente un sensor",
)
def update_sensor(
    sensor_id: str,
    sensor_update: SensorUpdate,
    db: Session = Depends(get_db),
    service: SensorService = Depends(get_sensor_service),
) -> SensorResponse:
    """Actualiza campos de un sensor sin tocar los no especificados."""
    return service.update_sensor(db, sensor_id, sensor_update)  # type: ignore[return-value]


@router.delete(
    "/{sensor_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Desactivar un sensor (Borrado lógico)",
)
def deactivate_sensor(
    sensor_id: str,
    db: Session = Depends(get_db),
    service: SensorService = Depends(get_sensor_service),
) -> None:
    """Desactiva el sensor para mantener integridad referencial histórica."""
    service.deactivate_sensor(db, sensor_id)