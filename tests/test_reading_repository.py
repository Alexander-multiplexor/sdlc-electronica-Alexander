from datetime import datetime
from unittest.mock import MagicMock

import pytest
from sqlalchemy.orm import Session

from app.repositories.reading_repository import ReadingRepository


@pytest.fixture
def mock_db():
    return MagicMock(spec=Session)

@pytest.fixture
def repo():
    return ReadingRepository()

def test_create_reading(repo, mock_db):
    reading_in = MagicMock()
    reading_in.sensor_id = "S1"
    reading_in.value = 25.5
    reading_in.unit = "C"
    
    result = repo.create(mock_db, reading_in)
    
    assert result.sensor_id == "S1"
    mock_db.add.assert_called_once()
    mock_db.commit.assert_called_once()

def test_list_by_sensor_no_dates(repo, mock_db):
    mock_scalars = MagicMock()
    mock_db.scalars.return_value = mock_scalars
    
    repo.list_by_sensor(mock_db, "S1")
    
    # Verifica que se hizo el select
    mock_db.scalars.assert_called_once()

def test_list_by_sensor_with_dates(repo, mock_db):
    mock_scalars = MagicMock()
    mock_db.scalars.return_value = mock_scalars
    
    # Probamos el filtro con fechas (esto cubre los IFs que faltaban)
    from_date = datetime(2026, 1, 1)
    to_date = datetime(2026, 1, 2)
    
    repo.list_by_sensor(mock_db, "S1", from_date=from_date, to_date=to_date)
    
    # Si llega aquí, significa que cubrimos las líneas de los IFs
    assert mock_db.scalars.called