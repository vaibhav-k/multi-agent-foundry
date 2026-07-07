"""
Planner agent.

Responsible for understanding user requests and preparing
future task decomposition logic.
"""

from __future__ import annotations

from .base import BaseAgent


class PlannerAgent(BaseAgent):
    """
    Agent responsible for planning user requests.
    """

    @property
    def name(self) -> str:
        """
        Agent identifier.

        Returns:
            Planner agent name.
        """

        return "PlannerAgent"

    @property
    def system_prompt(self) -> str:
        """
        Instructions for the planner.

        Returns:
            Planner system prompt.
        """

        return """
You are a planning agent.

Your responsibilities:

- Understand the user's intent.
- Identify required steps.
- Decide what information or actions may be needed.

For now, provide a concise explanation.
Future versions will delegate work to specialized agents.
"""
