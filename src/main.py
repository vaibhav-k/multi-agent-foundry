"""
Application entry point.

Runs the Day 1 Microsoft Foundry multi-agent sample.

Workflow

User
    ↓
Orchestrator
    ↓
PlannerAgent
    ↓
Azure AI Foundry
    ↓
Response
"""

from __future__ import annotations

from src.agents import PlannerAgent
from src.config import (
    CHAT_DEPLOYMENT,
    get_client,
)
from src.orchestrator import Orchestrator


def main() -> None:
    """
    Run the sample application.
    """

    client = get_client()

    planner = PlannerAgent(
        client=client,
        model=CHAT_DEPLOYMENT,
    )

    orchestrator = Orchestrator(
        planner=planner,
    )

    user_request = "Explain Microsoft Foundry in two sentences."

    response = orchestrator.run(
        user_request,
    )

    print(f"Agent   : {response.agent}")
    print(f"Response: {response.response}")


if __name__ == "__main__":
    main()
