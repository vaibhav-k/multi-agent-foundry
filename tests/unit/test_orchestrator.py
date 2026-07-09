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
        execution_steps=[
            "retrieve_documents",
            "generate_answer",
        ],
    )

    knowledge = Mock()

    knowledge.answer.return_value = GroundedAnswer(
        answer="Follow the VPN setup guide to configure access.",
        citations=[],
        grounded=True,
        confidence=0.9,
    )

    safety = Mock()

    safety.review.return_value = SafetyCheckResult(
        safe=True,
        reason="Response complies with policy.",
    )

    orchestrator = Orchestrator(
        planner=planner,
        knowledge_agent=knowledge,
        safety_agent=safety,
    )

    result = orchestrator.run("How do I connect VPN?")

    assert result.success is True

    assert result.planner_output is not None

    assert result.knowledge_output is not None

    assert result.safety_output is not None

    assert result.final_response is not None

    assert (
        result.final_response.answer
        == "Follow the VPN setup guide to configure access."
    )

    planner.plan.assert_called_once_with("How do I connect VPN?")

    knowledge.answer.assert_called_once_with(user_input="How do I connect VPN?")

    safety.review.assert_called_once_with(result.knowledge_output)
