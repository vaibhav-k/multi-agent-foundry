"""
Application configuration.

Loads Microsoft Foundry configuration from environment variables.

Environment Variables
---------------------
FOUNDRY_ENDPOINT
    Azure AI Foundry endpoint.

FOUNDRY_API_KEY
    API key used to authenticate requests.

CHAT_DEPLOYMENT
    Chat model deployment name.

EMBEDDING_DEPLOYMENT
    Embedding model deployment name.
"""

from __future__ import annotations

import os

from dotenv import load_dotenv

load_dotenv()


def _get_required_env(name: str) -> str:
    """
    Retrieve a required environment variable.

    Args:
        name:
            Name of the environment variable.

    Returns:
        Environment variable value.

    Raises:
        ValueError:
            If the environment variable is not defined.
    """

    value = os.getenv(name)

    if not value:
        raise ValueError(f"Environment variable '{name}' is not configured.")

    return value


FOUNDRY_ENDPOINT: str = _get_required_env("FOUNDRY_ENDPOINT")

FOUNDRY_API_KEY: str = _get_required_env("FOUNDRY_API_KEY")

CHAT_DEPLOYMENT: str = _get_required_env("CHAT_DEPLOYMENT")

EMBEDDING_DEPLOYMENT: str = _get_required_env("EMBEDDING_DEPLOYMENT")
