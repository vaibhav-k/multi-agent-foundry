"""
Tests for orchestrator workflow.
"""

from unittest.mock import Mock

from src.orchestrator.orchestrator import Orchestrator


def test_orchestrator_initialization():

    planner = Mock()

    orchestrator = Orchestrator(planner=planner)

    assert orchestrator.planner == planner


def test_orchestrator_calls_planner():

    planner = Mock()
    planner.plan.return_value = "plan"

    knowledge = Mock()
    knowledge.answer.return_value = "knowledge answer"

    safety = Mock()
    safety.review.return_value = "safe answer"

    orchestrator = Orchestrator(
        planner=planner,
        knowledge_agent=knowledge,
        safety_agent=safety,
    )

    result = orchestrator.run("How do I connect VPN?")

    planner.plan.assert_called_once_with("How do I connect VPN?")

    knowledge.answer.assert_called_once_with(user_input="How do I connect VPN?")

    safety.review.assert_called_once_with("knowledge answer")

    assert result.success is True
    assert result.final_response == "knowledge answer"
