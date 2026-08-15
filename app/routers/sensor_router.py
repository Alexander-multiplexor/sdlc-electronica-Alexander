from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.db import get_db
from app.schemas.sensor import SensorCreate, SensorResponse, SensorUpdate
from app.services.sensor_service import SensorService

router = APIRouter(
    prefix="/sensors",
    tags=["sensors"],
)


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
    """Registra un nuevo dispositivo en el sistema. Lanza 409 si ya existe."""
    try:
        return service.create_sensor(db, sensor_in)
    except HTTPException:
        raise
    except Exception as exc:
        msg = str(exc).lower()
        if "already exists" in msg or "duplicate" in msg or "unique" in msg:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Sensor {sensor_in.sensor_id} ya existe.",
            )
        raise


@router.get(
    "",
    response_model=List[SensorResponse],
    status_code=status.HTTP_200_OK,
    summary="Listar sensores con paginación",
)
def list_sensors(
    limit: int = Query(100, ge=1, le=500),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
    service: SensorService = Depends(get_sensor_service),
) -> List[SensorResponse]:
    """Lista sensores registrados con soporte para paginación."""
    return service.list_sensors(db, limit=limit, offset=offset)


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
    sensor = service.get_sensor(db, sensor_id)
    if not sensor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Sensor {sensor_id} no encontrado.",
        )
    return sensor


@router.patch(
    "/{sensor_id}",
    response_model=SensorResponse,
    status_code=status.HTTP_200_OK,
    summary="Actualizar un sensor",
)
def update_sensor(
    sensor_id: str,
    sensor_update: SensorUpdate,
    db: Session = Depends(get_db),
    service: SensorService = Depends(get_sensor_service),
) -> SensorResponse:
    """Actualiza parcialmente los datos de un sensor."""
    sensor = service.update_sensor(db, sensor_id, sensor_update)
    if not sensor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Sensor {sensor_id} no encontrado.",
        )
    return sensor


@router.delete(
    "/{sensor_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Desactivar un sensor",
)
def deactivate_sensor(
    sensor_id: str,
    db: Session = Depends(get_db),
    service: SensorService = Depends(get_sensor_service),
) -> None:
    """Desactiva un sensor lógicamente."""
    success = service.deactivate_sensor(db, sensor_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Sensor {sensor_id} no encontrado.",
        )
    return None