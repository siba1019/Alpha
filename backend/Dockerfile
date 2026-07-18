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

EXPOSE 8000

CMD ["/app/.venv/bin/uvicorn", "app.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
