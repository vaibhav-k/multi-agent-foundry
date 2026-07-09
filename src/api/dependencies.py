"""
FastAPI dependency providers.
"""

from functools import lru_cache

from src.orchestrator.orchestrator import AgentOrchestrator


@lru_cache
def get_orchestrator() -> AgentOrchestrator:
    """
    Return application orchestrator.

    Cached because the orchestrator owns reusable agent clients.
    """

    return AgentOrchestrator()
