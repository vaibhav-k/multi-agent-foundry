"""
Shared data models used throughout the application.

Contains:
- Agent contracts
- Conversation models
- Retrieval models
- RAG response models
- Safety models
- Planner models
- Evaluation models
- Workflow state models
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
    RESPONSE = "response"


class MessageRole(str, Enum):
    """Conversation roles."""

    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"


# ---------------------------------------------------------------------
# Conversation Models
# ---------------------------------------------------------------------


class ChatMessage(BaseModel):
    """
    Represents a single chat message.
    """

    role: MessageRole

    content: str


class AgentRequest(BaseModel):
    """
    Request sent to an agent.
    """

    user_query: str

    conversation_history: List[ChatMessage] = Field(default_factory=list)


# ---------------------------------------------------------------------
# Agent Response Models
# ---------------------------------------------------------------------


class DocumentReference(BaseModel):
    """
    Citation reference for generated responses.

    Represents supporting enterprise documentation.
    """

    document_id: Optional[str] = None

    name: str

    section: Optional[str] = None

    score: Optional[float] = None


class AgentResponse(BaseModel):
    """
    Standard response returned by every agent.

    All agents should return a consistent structure.
    """

    agent: AgentType

    response: str

    success: bool = True

    confidence: float = 0.0

    sources: List[DocumentReference] = Field(default_factory=list)

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

    section: Optional[str] = None


class RetrievalResult(BaseModel):
    """
    Collection of retrieved documents.

    Used by the Knowledge Agent.
    """

    query: str

    documents: List[RetrievedDocument] = Field(default_factory=list)


# ---------------------------------------------------------------------
# RAG Models
# ---------------------------------------------------------------------


class RAGContext(BaseModel):
    """
    Context provided to the answer generation step.
    """

    query: str

    documents: List[RetrievedDocument] = Field(default_factory=list)


class GroundedAnswer(BaseModel):
    """
    Final RAG-generated answer.

    Ensures answers are tied to enterprise sources.
    """

    answer: str

    citations: List[DocumentReference] = Field(default_factory=list)

    grounded: bool = True

    confidence: float = 0.0


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

    intent: Optional[str] = None


# ---------------------------------------------------------------------
# Agent State Models
# ---------------------------------------------------------------------


class AgentState(BaseModel):
    """
    Runtime state passed between agents.

    Tracks the complete execution lifecycle.
    """

    conversation_id: str

    user_query: str

    intent: Optional[str] = None

    retrieved_documents: List[RetrievedDocument] = Field(default_factory=list)

    safety_passed: bool = False

    response: Optional[GroundedAnswer] = None


# ---------------------------------------------------------------------
# Evaluation Models
# ---------------------------------------------------------------------


class EvaluationResult(BaseModel):
    """
    Used for RAG evaluation.

    Measures retrieval and answer quality.
    """

    question: str

    expected_answer: Optional[str] = None

    generated_answer: str

    expected_source: Optional[str] = None

    retrieved_sources: List[str] = Field(default_factory=list)

    grounded: bool

    retrieval_score: float

    answer_score: float

    citation_score: float = 0.0


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

    planner_output: Optional[PlannerDecision] = None

    knowledge_output: Optional[GroundedAnswer] = None

    safety_output: Optional[SafetyCheckResult] = None

    final_response: Optional[GroundedAnswer] = None

    success: bool = True

    metadata: dict = Field(default_factory=dict)
