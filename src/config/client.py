"""
Client factory.

Creates reusable Azure AI Foundry clients used throughout the application.
"""

from functools import lru_cache

from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential

from src.config.settings import get_settings


@lru_cache
def get_project_client() -> AIProjectClient:
    """
    Returns the Azure AI Foundry project client.

    The project client provides access to:
    - Model deployments
    - Azure OpenAI models
    - Azure AI Search connections
    - Other Foundry resources
    """

    settings = get_settings()

    return AIProjectClient(
        endpoint=settings.azure_ai_project_endpoint,
        credential=DefaultAzureCredential(),
    )


@lru_cache
def get_openai_client():
    """
    Returns the OpenAI-compatible client from Azure AI Foundry.

    Used for:
    - Chat completions
    - Responses API
    - Embeddings
    """

    project_client = get_project_client()

    return project_client.get_openai_client()


# ---------------------------------------------------------------
# Future service clients
# ---------------------------------------------------------------


@lru_cache
def get_search_client():
    """
    Returns Azure AI Search client.

    This will be enabled after the RAG pipeline is implemented.
    """

    settings = get_settings()

    from azure.search.documents import SearchClient
    from azure.core.credentials import AzureKeyCredential

    return SearchClient(
        endpoint=settings.azure_search_endpoint,
        index_name=settings.azure_search_index,
        credential=AzureKeyCredential(settings.azure_search_key),
    )


@lru_cache
def get_content_safety_client():
    """
    Returns Azure AI Content Safety client.

    This will be used by the Safety Agent.
    """

    settings = get_settings()

    from azure.ai.contentsafety import ContentSafetyClient
    from azure.core.credentials import AzureKeyCredential

    return ContentSafetyClient(
        endpoint=settings.azure_content_safety_endpoint,
        credential=AzureKeyCredential(settings.azure_content_safety_key),
    )
