import os
from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

# Usamos SQLite para desarrollo local, extensible a PostgreSQL para producción
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./sensorhub.db")

# check_same_thread=False es necesario únicamente para SQLite con FastAPI
engine = create_engine(
    DATABASE_URL, 
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    """Clase base tipada para SQLAlchemy 2.x"""
    pass


def get_db() -> Generator[Session, None, None]:
    """Inyector de dependencia para obtener la sesión de BD en FastAPI"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()