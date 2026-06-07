"""Shared response schemas used across multiple endpoints."""

from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    """GET /health response."""

    status: str = Field(default="healthy", examples=["healthy"])
    service: str = Field(default="OmniMind Backend", examples=["OmniMind Backend"])


class RootResponse(BaseModel):
    """GET / response."""

    message: str = Field(
        default="OmniMind Backend Running",
        examples=["OmniMind Backend Running"],
    )


class ErrorResponse(BaseModel):
    """Standard error envelope returned on failures."""

    success: bool = Field(default=False)
    error: str = Field(..., examples=["Message cannot be empty"])
