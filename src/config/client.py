"""
Azure client factory.

Provides:

- Azure AI Foundry Project Client
- Azure OpenAI Responses client
- Azure AI Foundry Embeddings client
- Azure AI Search client
- Azure AI Content Safety client
"""

from functools import lru_cache

from openai import OpenAI

from azure.ai.contentsafety import ContentSafetyClient
from azure.ai.inference import EmbeddingsClient
from azure.ai.projects import AIProjectClient
from azure.core.credentials import AzureKeyCredential
from azure.identity import DefaultAzureCredential
from azure.search.documents import SearchClient

from src.config.settings import get_settings


# =========================================================
# Azure Identity
# =========================================================

@lru_cache
def get_credential() -> DefaultAzureCredential:
    return DefaultAzureCredential()


# =========================================================
# Azure AI Foundry Project Client
# =========================================================

@lru_cache
def get_project_client() -> AIProjectClient:
    settings = get_settings()

    return AIProjectClient(
        endpoint=settings.azure_ai_project_endpoint,
        credential=get_credential(),
    )


# =========================================================
# Azure OpenAI Responses Client
# =========================================================

@lru_cache
def get_openai_client() -> OpenAI:
    """
    OpenAI-compatible client.

    Used by agents:
    - Planner
    - Knowledge
    - Safety

    Supports:
        client.responses.create()
    """

    settings = get_settings()

    return OpenAI(
        base_url=(
            f"{settings.azure_ai_project_endpoint}"
            "/openai/v1/"
        ),
        api_key=settings.azure_inference_key,
    )


# =========================================================
# Azure AI Foundry Embeddings Client
# =========================================================

@lru_cache
def get_embedding_client() -> EmbeddingsClient:
    """
    Azure AI Foundry embeddings.

    Used only for:
    - RAG ingestion
    - Vector generation
    """

    settings = get_settings()

    return EmbeddingsClient(
        endpoint=settings.azure_inference_endpoint,
        credential=AzureKeyCredential(
            settings.azure_inference_key
        ),
        model=settings.azure_openai_embedding_deployment,
    )


# =========================================================
# Azure AI Search
# =========================================================

@lru_cache
def get_search_client() -> SearchClient:
    settings = get_settings()

    return SearchClient(
        endpoint=settings.azure_search_endpoint,
        index_name=settings.azure_search_index,
        credential=AzureKeyCredential(
            settings.azure_search_key
        ),
    )


# =========================================================
# Azure AI Content Safety
# =========================================================

@lru_cache
def get_content_safety_client() -> ContentSafetyClient:
    settings = get_settings()

    return ContentSafetyClient(
        endpoint=settings.azure_content_safety_endpoint,
        credential=AzureKeyCredential(
            settings.azure_content_safety_key
        ),
    )