"""
Application orchestrator.

Coordinates interactions between the user and AI agents.

For Day 1, the orchestrator simply delegates all requests to the
PlannerAgent.

Future iterations will introduce routing between multiple agents,
including:

- PlannerAgent
- KnowledgeAgent
- ActionAgent
"""

from __future__ import annotations

from src.agents import PlannerAgent
from src.models import AgentResponse


class Orchestrator:
    """
    Coordinates AI agents.

    Attributes:
        planner:
            Planner agent responsible for processing requests.
    """

    def __init__(
        self,
        planner: PlannerAgent,
    ) -> None:
        """
        Initialize the orchestrator.

        Args:
            planner:
                Planner agent instance.
        """

        self.planner = planner

    def run(
        self,
        user_input: str,
    ) -> AgentResponse:
        """
        Execute the workflow.

        Args:
            user_input:
                User request.

        Returns:
            Response produced by the planner agent.
        """

        return self.planner.run(user_input)
