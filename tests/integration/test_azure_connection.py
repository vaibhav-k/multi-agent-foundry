"""
Azure AI Foundry connection integration test.

This test validates:
- Azure AI Foundry project authentication
- Model deployment availability
- Responses API connectivity

Run locally after configuring .env:

    pytest tests/test_azure_connection.py -s

For CI/CD, the test is skipped unless Azure configuration is available.
"""

import pytest

from src.config import get_openai_client, get_settings


def azure_configured() -> bool:
    """
    Check whether Azure AI Foundry configuration exists.
    """

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
    """
    Validate Azure AI Foundry model connectivity.
    """

    settings = get_settings()

    client = get_openai_client()

    response = client.responses.create(
        model=settings.azure_openai_chat_deployment,
        input="Hello. Confirm that the Enterprise IT Knowledge Assistant backend is working.",
    )

    assert response.output_text is not None
    assert len(response.output_text.strip()) > 0

    print("\nAzure AI Foundry response:")
    print(response.output_text)
