"""
OmniMind Backend — Application Entry Point.

Creates and configures the FastAPI application instance including:
- CORS middleware (allows React frontend communication)
- API routes
- Startup/shutdown lifecycle events
- Structured logging
- Custom exception handlers
"""

import logging
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.api.routes import router
from app.config.settings import get_settings
from app.schemas.common import ErrorResponse
from app.utils.logging_config import setup_logging

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Lifecycle (startup / shutdown)
# ---------------------------------------------------------------------------
@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Application lifespan handler — runs on startup and shutdown."""
    settings = get_settings()
    setup_logging(level=logging.DEBUG if settings.DEBUG else logging.INFO)
    logger.info(
        "Starting %s v%s", settings.PROJECT_NAME, settings.VERSION
    )
    yield
    logger.info("Shutting down %s", settings.PROJECT_NAME)


# ---------------------------------------------------------------------------
# App factory
# ---------------------------------------------------------------------------
def create_app() -> FastAPI:
    """Build and return the configured FastAPI application."""
    settings = get_settings()

    app = FastAPI(
        title=settings.PROJECT_NAME,
        version=settings.VERSION,
        description="Production-quality backend foundation for the OmniMind AI platform.",
        lifespan=lifespan,
    )

    # --- CORS ---
    origins = [
        "http://localhost:5173",  # Vite default
        "http://localhost:3000",  # CRA / Next.js default
    ]
    if settings.FRONTEND_URL not in origins:
        origins.append(settings.FRONTEND_URL)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        allow_headers=["*"],
    )

    # --- Routes ---
    app.include_router(router)

    # --- Exception handlers ---
    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(
        request: Request, exc: RequestValidationError
    ) -> JSONResponse:
        """Return a friendly error envelope on validation failures."""
        errors = exc.errors()
        first_msg = errors[0].get("msg", "Validation error") if errors else "Validation error"
        return JSONResponse(
            status_code=422,
            content=ErrorResponse(success=False, error=first_msg).model_dump(),
        )

    @app.exception_handler(Exception)
    async def generic_exception_handler(
        request: Request, exc: Exception
    ) -> JSONResponse:
        """Catch-all for unexpected server errors."""
        logger.exception("Unhandled exception: %s", exc)
        return JSONResponse(
            status_code=500,
            content=ErrorResponse(
                success=False, error="Internal server error"
            ).model_dump(),
        )

    return app


app = create_app()
