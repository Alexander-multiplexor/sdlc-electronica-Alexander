# --- ETAPA 1: Builder ---
FROM python:3.12-slim AS builder

WORKDIR /app

# Instalación de dependencias de sistema mínimas para compilar psycopg y utilidades
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copiar requerimientos e instalar paquetes en el directorio de usuario
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# --- ETAPA 2: Imagen Final de Producción (< 200 MB) ---
FROM python:3.12-slim

WORKDIR /app

# Copiar solo las librerías instaladas desde la etapa de compilación
COPY --from=builder /root/.local /root/.local
ENV PATH=/root/.local/bin:$PATH

# Copiar el código fuente
COPY . .

EXPOSE 8000

# Comando de arranque: ejecuta migraciones con Alembic antes de iniciar Uvicorn
CMD ["sh", "-c", "alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port 8000"]