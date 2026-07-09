"""
Azure AI Foundry connection integration test.

This test validates:
- Azure AI Foundry project authentication
- Model deployment availability
- Chat Completions API connectivity
"""

import pytest

from src.config import get_openai_client, get_settings


def azure_configured() -> bool:
    """Check whether Azure AI Foundry configuration exists."""
    try:
        settings = get_settings()
        return bool(
            settings.azure_ai_project_endpoint and settings.azure_openai_chat_deployment
        )
    except Exception:
        return False


@pytest.mark.integration
@pytest.mark.skipif(
    not azure_configured(),
    reason="Azure AI Foundry configuration not available",
)
def test_azure_foundry_connection():
    """Validate Azure AI Foundry model connectivity."""

    settings = get_settings()
    client = get_openai_client()

    response = client.chat.completions.create(
        model=settings.azure_openai_chat_deployment,
        messages=[
            {
                "role": "user",
                "content": "Reply with exactly the word OK.",
            }
        ],
        max_completion_tokens=10,
    )

    assert response.id
    assert response.model
    assert response.choices

    output_text = response.choices[0].message.content

    assert output_text is not None
    assert output_text.strip()
    assert response.choices[0].finish_reason == "stop"

    print(f"\n\nAzure AI Foundry response:\t{output_text}")
