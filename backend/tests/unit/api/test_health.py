"""Tests for operational API endpoints."""

import pytest
from app.api.main import create_app
from app.core.config import Settings
from httpx import ASGITransport, AsyncClient


@pytest.mark.anyio
async def test_health_check_returns_runtime_metadata() -> None:
    """Health checks should expose non-sensitive runtime metadata."""
    settings = Settings(app_name="test-alpha", environment="test", _env_file=None)
    transport = ASGITransport(app=create_app(settings))

    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "ok",
        "application": "test-alpha",
        "environment": "test",
    }
