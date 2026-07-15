"""
Base implementation for AI agents.

This module provides the common functionality shared by all agents in the
project, including:

- Loading system prompts from disk.
- Initializing the Azure AI Foundry client.
- Executing model inference.
- Logging agent activity.
- Returning generated responses.
"""

from pathlib import Path
from typing import Optional

from src.config import get_logger, get_openai_client, get_settings

logger = get_logger(__name__)


class BaseAgent:
    """
    Base class for all AI agents.

    The base agent encapsulates the common workflow for interacting with
    Azure AI Foundry language models. Concrete agent implementations inherit
    from this class and provide a different system prompt while reusing the
    shared inference pipeline.

    Attributes:
        name: Human-readable name of the agent.
        prompt_file: Filename of the system prompt stored in ``src/prompts``.
        settings: Application configuration loaded from the project's settings.
        client: Azure AI Foundry OpenAI client.
        system_prompt: Contents of the loaded system prompt.
    """

    def __init__(
        self,
        name: str,
        prompt_file: str,
    ):
        """
        Initialize the agent.

        Args:
            name: Human-readable identifier used for logging.
            prompt_file: Name of the prompt file located in ``src/prompts``.
        """
        self.name = name
        self.prompt_file = prompt_file

        self.settings = get_settings()
        self.client = get_openai_client()

        self.system_prompt = self._load_prompt(prompt_file)

        logger.info(f"Initialized agent: {self.name}")

    def _load_prompt(
        self,
        prompt_file: str,
    ) -> str:
        """
        Load the system prompt from disk.

        Args:
            prompt_file: Name of the prompt file located in ``src/prompts``.

        Returns:
            The prompt contents as a UTF-8 decoded string.

        Raises:
            FileNotFoundError: If the specified prompt file does not exist.
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
        Generate a response for a user request.

        The final prompt is constructed from the agent's system prompt, optional
        contextual information, and the user's request before being sent to the
        configured Azure AI Foundry model.

        Args:
            user_input: The user's request or instruction.
            context: Optional contextual information supplied by other agents or
                     previous processing stages.

        Returns: The generated response text from the language model.

        Raises:
            openai.PermissionDeniedError: If the configured credentials do not
                                          have permission to access the requested
                                          Azure AI Foundry deployment.
        """

        logger.info(f"{self.name} processing request")

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

        except PermissionDeniedError:
            logger.exception(f"{self.name} failed due to permission error")
            raise

        return response.output_text
