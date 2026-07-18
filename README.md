# Project Alpha

Project Alpha is a production-oriented foundation for Indian stock-market quantitative research. This repository intentionally contains **only Sprint 1 platform plumbing**: configuration, dependency boundaries, persistence, observability, a minimal health endpoint, quality checks, and deployment scaffolding. It contains no strategies, indicators, scanners, Pine Script, Chartink logic, UI, or live market-data integrations.

## Why uv

This project uses [uv](https://docs.astral.sh/uv/) for dependency and environment management. It is fast, produces a reproducible `uv.lock` file, supports Python version management, and uses the standard `pyproject.toml` ecosystem without a custom project model.

## Prerequisites

- Python 3.12 (the project intentionally supports the 3.12 release line)
- [uv](https://docs.astral.sh/uv/getting-started/installation/)
- Docker and Docker Compose (optional)

## Setup

```bash
uv python install 3.12
cd backend
uv sync --all-groups
cp ../.env.example ../.env
uv run pytest
```

Run the quality suite:

```bash
cd backend
uv run ruff check .
uv run ruff format --check .
uv run mypy app
uv run pytest
```

Format code with `uv run ruff format .` and fix eligible lint findings with `uv run ruff check . --fix`.

For the full local workflow, troubleshooting, and the rationale behind each foundation choice, see [the developer setup guide](docs/developer-setup.md).

## Configuration

Configuration is typed through `pydantic-settings`. Values are loaded from process environment and, for local development, `.env`. All variables are namespaced with `PROJECT_ALPHA_`.

| Variable | Default | Purpose |
| --- | --- | --- |
| `PROJECT_ALPHA_APP_NAME` | `project-alpha` | Service identifier in logs and tooling |
| `PROJECT_ALPHA_ENVIRONMENT` | `development` | Runtime environment name |
| `PROJECT_ALPHA_LOG_LEVEL` | `INFO` | Minimum application log level |
| `PROJECT_ALPHA_DATABASE_PATH` | `data/project_alpha.duckdb` | DuckDB database file |

Copy `.env.example` to `.env` for local overrides. Never commit `.env`.

## Architecture

The source tree follows Clean Architecture; dependencies point inward.

```text
backend/
  app/
    core/                 Typed settings and structured logging
    domain/               Enterprise business rules (currently empty)
    infrastructure/       DuckDB and future external-system adapters
    ingestion/            Data-ingestion contracts
    features/             Reserved for a future sprint
    backtest/             Reserved for a future sprint
    scanner/              Reserved for a future sprint
    strategies/           Reserved for a future sprint
    analytics/            Reserved for a future sprint
    api/                  Minimal FastAPI health endpoint
  tests/                  Unit tests organized by layer
  pyproject.toml          Backend dependency and quality configuration
pine/                     Pine Script workspace placeholder
chartink/                 Chartink workspace placeholder
notebooks/                Research notebook workspace placeholder
docs/                     Project documentation
data/                     Raw, processed, and DuckDB data directories
scripts/                  Operational script workspace placeholder
```

`DataIngestionPort` is an application-layer protocol. Future NSE, BSE, broker, or file adapters implement it in infrastructure without making business logic depend on a particular provider. `DuckDBDatabase` receives its path in its constructor, and settings should be assembled at a composition root before being injected into adapters. This keeps process state and infrastructure details outside application and domain code.

## Database

`DuckDBDatabase` owns connection lifecycle only; it does not contain research or business logic.

```python
from app.core.config import Settings
from app.infrastructure.database import DuckDBDatabase

settings = Settings()
database = DuckDBDatabase(settings.database_path)
database.initialize()

with database.connection() as connection:
    connection.execute("SELECT 1")
```

The adapter creates parent directories during initialization and yields a short-lived connection that is always closed.

## Logging

`configure_logging(settings.log_level)` configures JSON structured logs with an ISO-8601 UTC timestamp, log level, and context-variable support. Call it once from a future application entry point; libraries should obtain named loggers through `get_logger` and avoid configuring logging themselves.

## Health Endpoint

The only HTTP endpoint in Sprint 1 is `GET /health`. It returns non-sensitive application metadata and is intended for container orchestration and deployment checks. Start it locally with:

```bash
cd backend
uv run uvicorn app.api.main:app --host 0.0.0.0 --port 8000
```

## Docker

Build and run the foundation with:

```bash
docker compose up --build
```

The Compose file mounts `./data` so local DuckDB files persist outside the container. It loads `.env` when present; otherwise, the typed application defaults are used.

## Continuous Integration

GitHub Actions in `.github/workflows/ci.yml` runs Ruff linting, Ruff formatting verification, MyPy in strict mode, and pytest on pushes to `main` and all pull requests.

## Sprint Boundary

Sprint 1 establishes the platform foundation only. Market data retrieval, persistence schemas, research workflows, strategies, technical indicators, scanners, execution, and UI are deliberately out of scope.
