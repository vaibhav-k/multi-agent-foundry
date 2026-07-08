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

    planner.run.return_value = "response"

    orchestrator = Orchestrator(planner=planner)

    result = orchestrator.run("How do I connect VPN?")

    planner.run.assert_called_once_with("How do I connect VPN?")

    assert result == "response"
