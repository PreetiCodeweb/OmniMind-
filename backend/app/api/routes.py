"""
API route definitions.

All endpoints are defined here and mounted on the FastAPI app via the router.
"""

import logging

from fastapi import APIRouter

from app.schemas import (
    ChatRequest,
    ChatResponse,
    HealthResponse,
    RootResponse,
)

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/", response_model=RootResponse, tags=["General"])
async def root() -> RootResponse:
    """Root endpoint — confirms the server is reachable."""
    return RootResponse(message="OmniMind Backend Running")


@router.get("/health", response_model=HealthResponse, tags=["General"])
async def health_check() -> HealthResponse:
    """Health check used by monitoring tools and container orchestrators."""
    return HealthResponse(status="healthy", service="OmniMind Backend")


@router.post("/chat", response_model=ChatResponse, tags=["Chat"])
async def chat(payload: ChatRequest) -> ChatResponse:
    """
    Temporary chat endpoint.

    Echoes the received message back.  In future phases this will be
    replaced with actual AI model integration.
    """
    logger.info("Chat message received: %s", payload.message[:50])
    return ChatResponse(reply=f"Received: {payload.message}")
