import os
from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker


def get_database_url() -> str:
    """Obtiene y normaliza la URL de la base de datos para SQLite y PostgreSQL."""
    url = os.getenv("DATABASE_URL", "sqlite:///./sensorhub.db")
    if url.startswith("postgres://"):
        return url.replace("postgres://", "postgresql+psycopg://", 1)
    if url.startswith("postgresql://") and "+psycopg" not in url:
        return url.replace("postgresql://", "postgresql+psycopg://", 1)
    return url


# Asigna la URL procesada a DATABASE_URL
DATABASE_URL = get_database_url()

# check_same_thread=False solo se activa si la conexión es SQLite
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