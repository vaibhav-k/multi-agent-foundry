"""
Microsoft Foundry client.

Creates a reusable OpenAI client configured for Azure AI Foundry.
"""

from __future__ import annotations

from openai import OpenAI

from .settings import (
    FOUNDRY_API_KEY,
    FOUNDRY_ENDPOINT,
)


def get_client() -> OpenAI:
    """
    Create an OpenAI client.

    Returns:
        Configured OpenAI client.
    """

    return OpenAI(
        base_url=FOUNDRY_ENDPOINT,
        api_key=FOUNDRY_API_KEY,
    )
