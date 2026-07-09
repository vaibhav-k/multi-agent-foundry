"""
Agent execution state models.
"""

from pydantic import BaseModel, Field


class AgentState(BaseModel):
    """
    State passed between agents.
    """

    conversation_id: str

    user_message: str

    intent: str | None = None

    retrieved_documents: list[str] = Field(default_factory=list)

    safety_passed: bool = False

    response: str | None = None
