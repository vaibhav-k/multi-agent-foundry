"""
Shared data models.

This module contains common Pydantic models shared across the
application.
"""

from __future__ import annotations

from pydantic import BaseModel


class AgentResponse(BaseModel):
    """
    Standard response returned by an agent.

    Attributes:
        agent:
            Agent name.

        response:
            Natural language response produced by the agent.
    """

    agent: str

    response: str
