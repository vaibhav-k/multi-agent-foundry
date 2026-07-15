"""
Shared data models for the multi-agent knowledge assistant.

This module defines the strongly typed contracts exchanged between agents and
other application components. These models provide a consistent interface for
conversation management, retrieval, planning, safety validation, response
generation, evaluation, and workflow orchestration.

Model categories:
    - Agent contracts
    - Conversation models
    - Retrieval models
    - Retrieval-Augmented Generation (RAG) models
    - Planner models
    - Safety models
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
    """
    Enumeration of supported agent implementations.

    Used throughout the application to identify the origin of an agent
    response and to simplify logging, routing, and observability.
    """

    PLANNER = "planner"
    KNOWLEDGE = "knowledge"
    SAFETY = "safety"
    RESPONSE = "response"


class MessageRole(str, Enum):
    """
    Supported conversation message roles.

    Matches the standard chat-completion message roles used by modern
    large language model APIs.
    """

    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"


# ---------------------------------------------------------------------
# Conversation Models
# ---------------------------------------------------------------------


class ChatMessage(BaseModel):
    """
    Represents a single message within a conversation.

    Attributes:
        role:
            Role of the message sender.

        content:
            Natural language message content.
    """

    role: MessageRole

    content: str


class AgentRequest(BaseModel):
    """
    Request passed to an agent.

    Encapsulates the user's query together with the available conversation
    history, allowing agents to perform context-aware reasoning.
    """

    user_query: str

    conversation_history: List[ChatMessage] = Field(default_factory=list)


# ---------------------------------------------------------------------
# Agent Response Models
# ---------------------------------------------------------------------


class DocumentReference(BaseModel):
    """
    Reference to a supporting enterprise document.

    Citation metadata is attached to grounded responses so downstream
    consumers can display or audit the evidence used to generate an answer.

    Attributes:
        document_id: Unique document identifier.
        name: Human-readable document title.
        section: Optional section or heading within the document.
        score: Retrieval relevance score, when available.
    """

    document_id: Optional[str] = None

    name: str

    section: Optional[str] = None

    score: Optional[float] = None


class AgentResponse(BaseModel):
    """
    Standard response returned by an agent.

    Provides a consistent response contract across all agent
    implementations, including generated content, confidence,
    supporting sources, and optional metadata.
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
    Document retrieved from the enterprise search index.

    Represents a document returned during retrieval before it is supplied
    to the language model for grounded answer generation.
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

    Groups the original search query together with the ranked documents
    returned by the retrieval pipeline.
    """

    query: str

    documents: List[RetrievedDocument] = Field(default_factory=list)


# ---------------------------------------------------------------------
# RAG Models
# ---------------------------------------------------------------------


class RAGContext(BaseModel):
    """
    Context supplied to the answer generation stage.

    Combines the user's query with the retrieved documents that provide
    grounding for language model inference.
    """

    query: str

    documents: List[RetrievedDocument] = Field(default_factory=list)


class GroundedAnswer(BaseModel):
    """
    Grounded response produced by the knowledge agent.

    The generated answer is expected to be supported by one or more
    enterprise documents referenced through structured citations.

    Attributes:
        answer: Generated natural language response.
        citations: Supporting document references used during generation.
        grounded: Indicates whether the response is supported by
                  retrieved enterprise knowledge.
        confidence: Estimated confidence score for the generated answer.
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
    Result of the safety validation stage.

    Indicates whether a generated response satisfies the application's
    safety and compliance requirements before being returned to the user.
    """

    safe: bool

    reason: Optional[str] = None

    severity: Optional[str] = None


# ---------------------------------------------------------------------
# Planner Models
# ---------------------------------------------------------------------


class PlannerDecision(BaseModel):
    """
    Execution plan produced by the planner agent.

    Describes how the user request should be processed, including whether
    document retrieval or safety validation is required and the sequence
    of planned execution steps.
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
    Shared runtime state for agent execution.

    Stores information exchanged between agents during workflow execution
    and tracks the current state of the conversation pipeline.
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
    Evaluation metrics for Retrieval-Augmented Generation (RAG).

    Captures retrieval quality, answer quality, citation quality, and
    grounding metrics for offline benchmarking and regression testing.
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
    Complete result of a multi-agent workflow execution.

    Stores the intermediate outputs generated by each agent together with
    the final response returned to the user.

    This model is primarily intended for:
        - Workflow debugging
        - Offline evaluation
        - Observability and telemetry
        - Performance analysis
    """

    user_query: str

    planner_output: Optional[PlannerDecision] = None

    knowledge_output: Optional[GroundedAnswer] = None

    safety_output: Optional[SafetyCheckResult] = None

    final_response: Optional[GroundedAnswer] = None

    success: bool = True

    metadata: dict = Field(default_factory=dict)
