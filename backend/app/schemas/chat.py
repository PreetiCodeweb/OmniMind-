"""Pydantic models for the /chat endpoint."""

from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    """Incoming chat message from the frontend."""

    message: str = Field(
        ...,
        min_length=1,
        max_length=4096,
        description="The user's message to OmniMind.",
        examples=["Hello OmniMind"],
    )


class ChatResponse(BaseModel):
    """Temporary echo response (no AI integration yet)."""

    reply: str = Field(
        ...,
        description="Echo of the received message.",
        examples=["Received: Hello OmniMind"],
    )
