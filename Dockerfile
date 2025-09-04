# syntax=docker/dockerfile:1
FROM python:3.12-slim

# System deps (psycopg2 needs build tools & libpq-dev)
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl ca-certificates build-essential libpq-dev \
 && rm -rf /var/lib/apt/lists/*

# Install uv (https://astral.sh/uv)
ENV UV_LINK_MODE=copy
RUN curl -fsSL https://astral.sh/uv/install.sh | sh
ENV PATH="/root/.local/bin:${PATH}"

WORKDIR /app

# Cache layer for deps
COPY requirements.txt ./
RUN uv pip install --system --no-cache -r requirements.txt

# App code
COPY app ./app

# Non-root user & writable uploads dir
RUN useradd -m appuser \
 && mkdir -p /app/uploads \
 && chown -R appuser:appuser /app
USER appuser

ENV PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    FLASK_ENV=production \
    UPLOAD_DIR=/app/uploads

EXPOSE 8000

# Gunicorn entrypoint
CMD ["gunicorn", "app:create_app()", "-b", "0.0.0.0:8000", "-w", "2"]
