"""
Embedding connectivity test.

Validates that the embedding deployment can generate vectors.
"""

from __future__ import annotations

from openai import OpenAI

from src.config import (
    EMBEDDING_DEPLOYMENT,
    FOUNDRY_ENDPOINT,
    FOUNDRY_API_KEY,
)


def get_embedding_client() -> OpenAI:
    """
    Create Foundry client for embeddings.

    Returns:
        OpenAI client configured for Azure AI Foundry.
    """

    return OpenAI(
        base_url=FOUNDRY_ENDPOINT,
        api_key=FOUNDRY_API_KEY,
    )


def test_embedding_connection() -> None:
    """
    Verify embedding model connectivity.
    """

    client = get_embedding_client()

    response = client.embeddings.create(
        model=EMBEDDING_DEPLOYMENT,
        input="What is Azure AI Foundry?",
    )

    vector = response.data[0].embedding

    assert vector

    assert len(vector) > 0