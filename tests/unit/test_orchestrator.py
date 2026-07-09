"""
Tests for orchestrator workflow.
"""

from unittest.mock import Mock

from src.models import (
    GroundedAnswer,
    PlannerDecision,
    SafetyCheckResult,
)
from src.orchestrator.orchestrator import Orchestrator


def test_orchestrator_initialization():

    planner = Mock()

    orchestrator = Orchestrator(planner=planner)

    assert orchestrator.planner == planner


def test_orchestrator_calls_planner():

    planner = Mock()

    planner.plan.return_value = PlannerDecision(
        requires_retrieval=True,
        requires_safety_review=True,
        execution_steps=["retrieve_documents"],
        intent="vpn_configuration",
    )

    knowledge = Mock()

    knowledge.answer.return_value = GroundedAnswer(
        answer="VPN setup instructions",
        grounded=True,
        confidence=0.9,
    )

    safety = Mock()

    safety.review.return_value = SafetyCheckResult(
        safe=True,
        reason="Approved",
    )

    orchestrator = Orchestrator(
        planner=planner,
        knowledge_agent=knowledge,
        safety_agent=safety,
    )

    result = orchestrator.run("How do I connect VPN?")

    assert result.success is True

    planner.plan.assert_called_once()

    knowledge.answer.assert_called_once()

    safety.review.assert_called_once()
