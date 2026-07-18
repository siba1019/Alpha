# Developer Setup Guide

## Purpose

This guide explains how to work on Project Alpha during Sprint 1. The sprint deliberately provides platform infrastructure only; do not add strategies, scanners, technical indicators, Pine Script, Chartink logic, or research workflows here.

## Local Setup

1. Install Python 3.12 and [uv](https://docs.astral.sh/uv/getting-started/installation/).
2. From the repository root, run `uv python install 3.12`.
3. Run `cp .env.example .env` to create local configuration.
4. Change to `backend` and run `uv sync --all-groups`.
5. Run `uv run pytest` to validate the installation.

`uv.lock` is committed. Use `uv sync --locked --all-groups` in CI and reproducible environments; update the lock deliberately with `uv lock` when dependencies change.

## Daily Commands

Run these commands from `backend`:

```bash
uv run ruff check .
uv run ruff format --check .
uv run mypy app
uv run pytest
uv run uvicorn app.api.main:app --reload
```

Use `uv run ruff format .` before committing formatted code. The project requires Python 3.12, strict MyPy checks, and at least 90% coverage of executable production code.

## Configuration

`app.core.config.Settings` uses Pydantic Settings. Environment variables are the source of truth; `.env` is only a local-development convenience. The `PROJECT_ALPHA_` prefix prevents accidental collisions with other processes. Do not log or commit credentials. Add future settings as typed fields with conservative defaults.

## Design Decisions

| Decision | Rationale |
| --- | --- |
| Python 3.12 only | A single supported runtime removes version-dependent behavior and keeps CI, containers, and developer machines aligned. |
| uv and committed lockfile | Fast resolution plus deterministic dependency installation. |
| Clean Architecture folders | Domain concerns remain independent from adapters such as DuckDB, FastAPI, and future data providers. |
| FastAPI health endpoint only | It establishes an operational HTTP boundary without prematurely designing a research or trading API. |
| Dependency-injected settings | Tests and embedding processes supply settings explicitly; infrastructure does not read environment state itself. |
| DuckDB adapter owns connection lifecycle | Persistence details stay outside domain logic and connections are deterministically closed. |
| Protocol-based ingestion contract | Future providers can be swapped without coupling the application to NSE, BSE, broker, or file implementations. |
| JSON structured logging | Logs are queryable in local and hosted environments and retain contextual fields. |
| Ruff plus strict MyPy | Fast static feedback catches style, import, typing, and common correctness issues before runtime. |
| Pytest with coverage threshold | Foundation behavior remains verifiable as the project expands. |
| Docker and GitHub Actions | The same locked dependency set is checked in CI and can be run in a container. |

## Testing Expectations

Every executable module needs public functions or methods with type hints and Google-style docstrings. Add focused unit tests for each behavior and emit structured logs at meaningful infrastructure or request boundaries. Placeholder packages are intentionally documentation-only until their sprint begins.

## Docker

From the repository root, run `docker compose up --build`. The service exposes `GET http://localhost:8000/health` and mounts `data/` into the container so DuckDB files persist locally. Docker uses the backend lockfile with `uv sync --locked`; Compose loads `.env` when available and otherwise uses the application defaults.

## Continuous Integration

The workflow runs from `backend` and executes lockfile validation, Ruff linting, formatting checks, strict MyPy, and pytest. A pull request should be green before merge.
