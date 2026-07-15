"""
Unit tests for PlannerAgent.
"""

from unittest.mock import patch

from src.agents.planner import PlannerAgent
from src.models import PlannerDecision


def test_planner_returns_execution_plan():

    with patch(
        "src.agents.base.BaseAgent.run",
        return_value="retrieval workflow required",
    ):

        agent = PlannerAgent()

        result = agent.plan("How do I connect to the company VPN?")

    assert isinstance(
        result,
        PlannerDecision,
    )

    assert result.requires_retrieval is True

    assert result.requires_safety_review is True

    assert "retrieve_documents" in result.execution_steps

    assert "generate_grounded_answer" in result.execution_steps

    assert "validate_safety" in result.execution_steps


def test_planner_handles_general_question():

    with patch(
        "src.agents.base.BaseAgent.run",
        return_value="simple response",
    ):

        agent = PlannerAgent()

        result = agent.plan("What is the company working culture?")

    assert isinstance(
        result,
        PlannerDecision,
    )

    # Current implementation uses deterministic routing.
    # This test documents current expected behavior.
    assert result.requires_retrieval is True


def test_planner_initialization():

    with patch(
        "src.agents.base.BaseAgent.run",
        return_value="",
    ):

        agent = PlannerAgent()

    assert agent.name == "PlannerAgent"

    assert agent.prompt_file == "planner.txt"


def test_planner_requires_retrieval_for_it_questions():

    planner = PlannerAgent()

    result = planner._parse_plan("""
        {
            "intent": "MFA configuration",
            "requires_retrieval": false,
            "requires_safety_review": false,
            "execution_steps": []
        }
        """)

    assert result.requires_retrieval is True
    assert result.requires_safety_review is True
