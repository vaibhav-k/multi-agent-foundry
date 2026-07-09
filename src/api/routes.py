"""
HTTP API routes.

Provides chat and health endpoints.
"""

from fastapi import APIRouter, Depends

from src.api.dependencies import get_orchestrator
from src.api.schemas import ChatRequest, ChatResponse
from src.orchestrator.orchestrator import AgentOrchestrator

router = APIRouter()


@router.get("/health")
def health_check():
    """
    Application health endpoint.
    """

    return {"status": "healthy"}


@router.post(
    "/chat",
    response_model=ChatResponse,
)
def chat(
    request: ChatRequest,
    orchestrator: AgentOrchestrator = Depends(get_orchestrator),
):
    """
    Process a user question.

    Flow:

    User
      |
    Planner Agent
      |
    Knowledge Agent
      |
    Safety Agent
      |
    Response
    """

    result = orchestrator.run(
        conversation_id=request.conversation_id,
        message=request.message,
    )

    return ChatResponse(
        conversation_id=request.conversation_id,
        answer=result.answer,
        sources=result.sources,
    )
