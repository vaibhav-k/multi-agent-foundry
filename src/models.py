"""
Shared data models used throughout the application.
"""

from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field

# ---------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------


class AgentType(str, Enum):
    """Supported agent types."""

    PLANNER = "planner"
    KNOWLEDGE = "knowledge"
    SAFETY = "safety"


class MessageRole(str, Enum):
    """Conversation roles."""

    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"


# ---------------------------------------------------------------------
# Conversation Models
# ---------------------------------------------------------------------


class ChatMessage(BaseModel):
    """Represents a single chat message."""

    role: MessageRole
    content: str


class AgentRequest(BaseModel):
    """
    Request sent to an agent.
    """

    user_query: str
    conversation_history: List[ChatMessage] = Field(default_factory=list)


class AgentResponse(BaseModel):
    """
    Standard response returned by every agent.
    """

    agent: AgentType

    response: str

    success: bool = True

    metadata: dict = Field(default_factory=dict)


# ---------------------------------------------------------------------
# Retrieval Models
# ---------------------------------------------------------------------


class RetrievedDocument(BaseModel):
    """
    Document returned from Azure AI Search.
    """

    document_id: str

    title: str

    content: str

    score: float

    source: Optional[str] = None


class RetrievalResult(BaseModel):
    """
    Collection of retrieved documents.
    """

    query: str

    documents: List[RetrievedDocument]


# ---------------------------------------------------------------------
# Safety Models
# ---------------------------------------------------------------------


class SafetyCheckResult(BaseModel):
    """
    Result returned by the Safety Agent.
    """

    safe: bool

    reason: Optional[str] = None

    severity: Optional[str] = None


# ---------------------------------------------------------------------
# Planner Models
# ---------------------------------------------------------------------


class PlannerDecision(BaseModel):
    """
    Planner output describing the execution plan.
    """

    requires_retrieval: bool = False

    requires_safety_review: bool = True

    execution_steps: List[str] = Field(default_factory=list)


# ---------------------------------------------------------------------
# Evaluation Models
# ---------------------------------------------------------------------


class EvaluationResult(BaseModel):
    """
    Used for RAG evaluation.
    """

    question: str

    expected_answer: str

    generated_answer: str

    grounded: bool

    retrieval_score: float

    answer_score: float


# ---------------------------------------------------------------------
# Multi-Agent Workflow Models
# ---------------------------------------------------------------------


class AgentWorkflowResult(BaseModel):
    """
    Complete execution result from the multi-agent workflow.

    Stores intermediate outputs for:
    - Planner
    - Knowledge
    - Safety
    - Final response

    Useful for:
    - Debugging
    - Evaluation
    - Observability
    """

    user_query: str

    planner_output: Optional[str] = None

    knowledge_output: Optional[str] = None

    safety_output: Optional[str] = None

    final_response: Optional[str] = None

    success: bool = True

    metadata: dict = Field(default_factory=dict)
