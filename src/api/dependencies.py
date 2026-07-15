"""
FastAPI dependency providers.
"""

from functools import lru_cache

from src.bootstrap import create_orchestrator
from src.orchestrator.orchestrator import Orchestrator


@lru_cache
def get_orchestrator() -> Orchestrator:
    """
    Return a singleton orchestrator instance.
    """

    return create_orchestrator()
