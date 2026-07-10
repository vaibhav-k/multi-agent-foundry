"""
Azure client factory.

Creates reusable Azure clients.

Clients:

- Azure AI Foundry Project Client
- Azure AI Foundry OpenAI Responses Client
- Azure AI Foundry Embeddings Client
- Azure AI Search Client
- Azure AI Content Safety Client
"""

from functools import lru_cache

from azure.ai.contentsafety import ContentSafetyClient
from azure.ai.inference import EmbeddingsClient
from azure.ai.projects import AIProjectClient
from azure.core.credentials import AzureKeyCredential
from azure.identity import (
    DefaultAzureCredential,
    get_bearer_token_provider,
)
from azure.search.documents import SearchClient
from openai import OpenAI

from src.config.settings import get_settings

# =========================================================
# Azure Identity
# =========================================================


@lru_cache
def get_credential() -> DefaultAzureCredential:
    """
    Shared Azure credential.

    Authentication chain:

    - EnvironmentCredential
    - Managed Identity
    - Azure CLI
    - VS Code credential
    """

    return DefaultAzureCredential()


# =========================================================
# Azure AI Foundry Project Client
# =========================================================


@lru_cache
def get_project_client() -> AIProjectClient:
    """
    Azure AI Foundry project client.

    Used for:
    - deployments
    - connections
    - project resources
    """

    settings = get_settings()

    return AIProjectClient(
        endpoint=settings.azure_ai_project_endpoint,
        credential=get_credential(),
    )


# =========================================================
# Azure AI Foundry OpenAI Responses Client
# =========================================================


@lru_cache
def get_openai_client() -> OpenAI:
    """
    Azure AI Foundry OpenAI-compatible client.

    Used by agents:

    - PlannerAgent
    - KnowledgeAgent
    - SafetyAgent

    Supports:
    - Responses API
    """

    settings = get_settings()

    token_provider = get_bearer_token_provider(
        get_credential(),
        "https://ai.azure.com/.default",
    )

    return OpenAI(
        base_url=(f"{settings.azure_ai_project_endpoint.rstrip('/')}" "/openai/v1"),
        api_key=token_provider,
    )


# =========================================================
# Azure AI Foundry Embeddings Client
# =========================================================


@lru_cache
def get_embedding_client() -> EmbeddingsClient:
    """
    Azure AI Foundry embedding client.

    Used by RAG ingestion.

    Model:
    - text-embedding-3-small
    """

    settings = get_settings()

    return EmbeddingsClient(
        endpoint=settings.azure_inference_endpoint,
        credential=AzureKeyCredential(settings.azure_inference_key),
        model=settings.azure_openai_embedding_deployment,
    )


# compatibility
get_openai_client = get_embedding_client


# =========================================================
# Azure AI Search
# =========================================================


@lru_cache
def get_search_client() -> SearchClient:
    """
    Azure AI Search client.

    Used for:
    - document indexing
    - vector search
    """

    settings = get_settings()

    return SearchClient(
        endpoint=settings.azure_search_endpoint,
        index_name=settings.azure_search_index,
        credential=AzureKeyCredential(settings.azure_search_key),
    )


# =========================================================
# Azure AI Content Safety
# =========================================================


@lru_cache
def get_content_safety_client() -> ContentSafetyClient:
    """
    Azure AI Content Safety client.
    """

    settings = get_settings()

    return ContentSafetyClient(
        endpoint=settings.azure_content_safety_endpoint,
        credential=AzureKeyCredential(settings.azure_content_safety_key),
    )
