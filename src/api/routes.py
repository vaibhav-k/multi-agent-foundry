"""
HTTP API routes.

Provides chat and health endpoints.
"""

from fastapi import APIRouter, Depends

from src.api.dependencies import get_orchestrator
from src.api.schemas import ChatRequest, ChatResponse
from src.orchestrator.orchestrator import Orchestrator

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
    orchestrator: Orchestrator = Depends(get_orchestrator),
):
    """
    Process a user question.
    """

    result = orchestrator.run(
        user_input=request.message,
        conversation_id=request.conversation_id,
    )

    knowledge = result.knowledge_output
    safety = result.safety_output
    final = result.final_response

    sources = []

    if knowledge and knowledge.citations:
        sources = [citation.document_id for citation in knowledge.citations]

    return ChatResponse(
        conversation_id=request.conversation_id,
        answer=(final.answer if final else "No response generated."),
        sources=sources,
        confidence=(knowledge.confidence if knowledge else 0.0),
        grounded=(knowledge.grounded if knowledge else False),
        safe=(safety.safe if safety else False),
    )
