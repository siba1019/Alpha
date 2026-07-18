"""FastAPI composition root and operational health endpoint."""

from typing import Annotated

from fastapi import Depends, FastAPI
from pydantic import BaseModel

from app.core.config import Settings
from app.core.logging.setup import configure_logging, get_logger


class HealthResponse(BaseModel):
    """Public response returned by the service health endpoint."""

    status: str
    application: str
    environment: str


def create_app(settings: Settings | None = None) -> FastAPI:
    """Create a configured FastAPI application using injected runtime settings.

    Args:
        settings: Optional explicit settings for tests or an embedding process.
            When omitted, settings are read at the application composition root.

    Returns:
        A FastAPI application exposing operational endpoints only.
    """
    runtime_settings = settings or Settings()
    configure_logging(runtime_settings.log_level)
    logger = get_logger(__name__)
    application = FastAPI(title=runtime_settings.app_name, version="0.1.0")

    def get_settings() -> Settings:
        """Provide the immutable runtime settings to endpoint handlers."""
        return runtime_settings

    @application.get("/health", response_model=HealthResponse, tags=["operations"])
    def health_check(
        active_settings: Annotated[Settings, Depends(get_settings)],
    ) -> HealthResponse:
        """Report whether the application process is able to serve requests."""
        logger.info("health_check_requested", environment=active_settings.environment)
        return HealthResponse(
            status="ok",
            application=active_settings.app_name,
            environment=active_settings.environment,
        )

    return application


app = create_app()
