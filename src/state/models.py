"""
Agent execution state models.

Defines the shared runtime state passed
between Planner, Knowledge, and Safety agents.
"""

from typing import Optional, List

from pydantic import BaseModel, Field

from src.models import (
    ChatMessage,
    GroundedAnswer,
    PlannerDecision,
    SafetyCheckResult,
)


class AgentState(BaseModel):
    """
    State passed between agents during execution.

    Lifecycle:

    User Request
          |
          v
    Planner Decision
          |
          v
    Knowledge Retrieval
          |
          v
    Safety Validation
          |
          v
    Final Response
    """

    # -------------------------------------------------
    # Conversation
    # -------------------------------------------------

    conversation_id: str

    user_message: str

    conversation_history: List[ChatMessage] = Field(default_factory=list)

    # -------------------------------------------------
    # Planner
    # -------------------------------------------------

    planner_decision: Optional[PlannerDecision] = None

    intent: Optional[str] = None

    # -------------------------------------------------
    # Knowledge Agent
    # -------------------------------------------------

    retrieved_documents: list[str] = Field(default_factory=list)

    knowledge_response: Optional[GroundedAnswer] = None

    # -------------------------------------------------
    # Safety Agent
    # -------------------------------------------------

    safety_result: Optional[SafetyCheckResult] = None

    safety_passed: bool = False

    # -------------------------------------------------
    # Final Output
    # -------------------------------------------------

    response: Optional[str] = None

    final_answer: Optional[GroundedAnswer] = None

    # -------------------------------------------------
    # Runtime metadata
    # -------------------------------------------------

    metadata: dict = Field(default_factory=dict)
