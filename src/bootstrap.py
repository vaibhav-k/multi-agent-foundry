"""
Application bootstrap.

Constructs and wires together the application's dependencies.

This module centralizes dependency creation so the application entry
points (CLI, API, tests) can all obtain a fully configured
Orchestrator from one place.
"""

from src.agents import (
    KnowledgeAgent,
    PlannerAgent,
    SafetyAgent,
)
from src.orchestrator import Orchestrator


def create_orchestrator() -> Orchestrator:
    """
    Create and configure the application orchestrator.

    Returns:
        A fully initialized Orchestrator instance.
    """
    planner = PlannerAgent()
    knowledge_agent = KnowledgeAgent()
    safety_agent = SafetyAgent()

    return Orchestrator(
        planner=planner,
        knowledge_agent=knowledge_agent,
        safety_agent=safety_agent,
    )
