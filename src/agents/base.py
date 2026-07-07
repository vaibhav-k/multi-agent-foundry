"""
Base agent implementation.

Provides shared LLM communication functionality for all agents.

Individual agents only need to define:
- agent name
- system prompt
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from openai import OpenAI

from src.models import AgentResponse


class BaseAgent(ABC):
    """
    Abstract base class for AI agents.

    This class owns communication with Azure AI Foundry.

    Child classes only define:
    - their identity
    - their system instructions
    """

    def __init__(
        self,
        client: OpenAI,
        model: str,
    ) -> None:
        """
        Initialize an agent.

        Args:
            client:
                Azure AI Foundry OpenAI client.

            model:
                Chat model deployment name.
        """

        self.client = client
        self.model = model

    @property
    @abstractmethod
    def name(self) -> str:
        """
        Agent name.

        Returns:
            Name of the agent.
        """

    @property
    @abstractmethod
    def system_prompt(self) -> str:
        """
        Agent instructions.

        Returns:
            System prompt used by the model.
        """

    def run(
        self,
        user_input: str,
    ) -> AgentResponse:
        """
        Execute the agent.

        Args:
            user_input:
                User request.

        Returns:
            Standard agent response.
        """

        response = self.client.responses.create(
            model=self.model,
            input=[
                {
                    "role": "system",
                    "content": self.system_prompt,
                },
                {
                    "role": "user",
                    "content": user_input,
                },
            ],
        )

        return AgentResponse(
            agent=self.name,
            response=response.output_text,
        )
