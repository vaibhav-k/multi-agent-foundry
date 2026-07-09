"""
API request and response schemas.
"""

from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    """
    User chat request.
    """

    conversation_id: str = Field(description="Unique conversation identifier.")

    message: str = Field(description="User question or request.")


class ChatResponse(BaseModel):
    """
    Assistant response.
    """

    conversation_id: str

    answer: str

    sources: list[str] = Field(
        default_factory=list, description="Supporting knowledge sources."
    )
