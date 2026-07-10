"""
Base agent implementation.

Provides shared functionality for all agents:
- Prompt loading
- Azure AI Foundry model invocation
- Logging
- Standard response handling
"""

from pathlib import Path
from typing import Optional

from src.config import get_logger, get_openai_client, get_settings

logger = get_logger(__name__)


class BaseAgent:
    """
    Base class for all AI agents.

    All agents:
    - Use Azure AI Foundry models
    - Have a system prompt
    - Receive user input
    - Return generated responses
    """

    def __init__(
        self,
        name: str,
        prompt_file: str,
    ):
        self.name = name
        self.prompt_file = prompt_file

        self.settings = get_settings()
        self.client = get_openai_client()

        self.system_prompt = self._load_prompt(prompt_file)

        logger.info(
            "Initialized agent: %s",
            self.name,
        )

    def _load_prompt(
        self,
        prompt_file: str,
    ) -> str:
        """
        Load agent system prompt from file.
        """

        prompt_path = Path("src") / "prompts" / prompt_file

        if not prompt_path.exists():
            raise FileNotFoundError(f"Prompt not found: {prompt_path}")

        return prompt_path.read_text(encoding="utf-8")

    def run(
        self,
        user_input: str,
        context: Optional[str] = None,
    ) -> str:
        """
        Execute the agent.

        Args:
            user_input:
                User request.

            context:
                Optional context from other agents.

        Returns:
            Generated response text.
        """

        logger.info(
            "%s processing request",
            self.name,
        )

        prompt_parts = []

        # System instructions
        prompt_parts.append(self.system_prompt)

        # Optional context
        if context:

            prompt_parts.append(f"""
    Additional context:

    {context}
    """)

        # User request
        prompt_parts.append(f"""
    User request:

    {user_input}
    """)

        final_prompt = "\n\n".join(prompt_parts)

        from openai import PermissionDeniedError

        try:
            response = self.client.responses.create(
                model=self.settings.azure_openai_chat_deployment,
                input=final_prompt,
            )
        except PermissionDeniedError as e:
            print("Status:", e.status_code)
            print("Body:", e.response.text)
            raise

        return response.output_text
