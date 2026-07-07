"""
Chat connectivity test.

Validates that the Microsoft Foundry chat deployment
is reachable and can return a response.
"""

from __future__ import annotations

from src.agents import PlannerAgent
from src.config import (
    CHAT_DEPLOYMENT,
    get_client,
)


def test_chat_connection() -> None:
    """
    Verify chat model connectivity.

    This test requires:
        - Valid Foundry endpoint
        - Valid API key
        - Existing chat deployment
    """

    client = get_client()

    agent = PlannerAgent(
        client=client,
        model=CHAT_DEPLOYMENT,
    )

    response = agent.run(
        "Explain Azure AI Foundry in one sentence."
    )

    assert response.agent == "PlannerAgent"

    assert response.response
