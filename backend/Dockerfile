FROM python:3.12-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    UV_LINK_MODE=copy

WORKDIR /app

RUN pip install --no-cache-dir "uv>=0.5,<1"

COPY backend/pyproject.toml backend/uv.lock backend/README.md ./

RUN uv sync --locked --no-dev --no-install-project

COPY backend/app ./app

RUN uv sync --locked --no-dev

CMD ["/app/.venv/bin/python", "-c", "from app.core.config import Settings; print(Settings().app_name)"]
