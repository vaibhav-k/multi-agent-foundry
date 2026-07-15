"""
Tests for ResponseAgent.
"""

from src.agents.response import ResponseAgent
from src.models import (
    GroundedAnswer,
    PlannerDecision,
    SafetyCheckResult,
)


def test_response_agent_returns_safe_response():
    """
    ResponseAgent should return the knowledge response
    when safety validation passes.
    """

    agent = ResponseAgent()

    knowledge_response = GroundedAnswer(
        answer="VPN setup instructions",
        citations=[],
        grounded=True,
        confidence=1.0,
    )

    safety_result = SafetyCheckResult(
        safe=True,
        reason="Response passed safety validation.",
        severity="low",
    )

    planner_decision = PlannerDecision(
        requires_retrieval=True,
        requires_safety_review=True,
        execution_steps=[
            "retrieve_documents",
            "generate_grounded_answer",
            "validate_safety",
        ],
    )

    result = agent.generate(
        planner_decision=planner_decision,
        knowledge_response=knowledge_response,
        safety_result=safety_result,
    )

    assert result is not None
    assert result.answer == "VPN setup instructions"
    assert result.grounded is True


def test_response_agent_blocks_unsafe_response():
    """
    ResponseAgent should reject responses that fail safety validation.
    """

    agent = ResponseAgent()

    knowledge_response = GroundedAnswer(
        answer="Unsafe answer",
        citations=[],
        grounded=True,
        confidence=0.8,
    )

    safety_result = SafetyCheckResult(
        safe=False,
        reason="Failed safety validation.",
        severity="high",
    )

    result = agent.generate(
        planner_decision=None,
        knowledge_response=knowledge_response,
        safety_result=safety_result,
    )

    assert result is None


def test_response_agent_handles_missing_knowledge_response():
    """
    ResponseAgent should handle missing knowledge output.
    """

    agent = ResponseAgent()

    result = agent.generate(
        planner_decision=None,
        knowledge_response=None,
        safety_result=None,
    )

    assert result is None
