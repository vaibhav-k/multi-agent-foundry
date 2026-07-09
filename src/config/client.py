"""
Client factory.

Creates reusable Azure clients used throughout the application.
"""

from functools import lru_cache

import openai

from azure.ai.contentsafety import ContentSafetyClient
from azure.ai.projects import AIProjectClient
from azure.core.credentials import AzureKeyCredential
from azure.identity import DefaultAzureCredential, get_bearer_token_provider
from azure.search.documents import SearchClient

from src.config.settings import get_settings


@lru_cache
def get_project_client() -> AIProjectClient:
    """
    Returns an authenticated Azure AI Foundry project client.
    """
    settings = get_settings()

    return AIProjectClient(
        endpoint=settings.azure_ai_project_endpoint,
        credential=DefaultAzureCredential(),
    )


@lru_cache
def get_openai_client() -> openai.OpenAI:
    """
    Returns an OpenAI-compatible client for Azure AI Foundry.

    This client can be used for:
    - Chat completions
    - Responses API
    - Embeddings
    """

    settings = get_settings()

    token_provider = get_bearer_token_provider(
        DefaultAzureCredential(),
        "https://ai.azure.com/.default",
    )

    return openai.OpenAI(
        base_url=f"{settings.azure_ai_project_endpoint.rstrip('/')}/openai/v1",
        api_key=token_provider,
    )


# Backwards-compatible alias
get_embedding_client = get_openai_client


@lru_cache
def get_search_client() -> SearchClient:
    """
    Returns an Azure AI Search client.
    """
    settings = get_settings()

    return SearchClient(
        endpoint=settings.azure_search_endpoint,
        index_name=settings.azure_search_index,
        credential=AzureKeyCredential(settings.azure_search_key),
    )


@lru_cache
def get_content_safety_client() -> ContentSafetyClient:
    """
    Returns an Azure AI Content Safety client.
    """
    settings = get_settings()

    return ContentSafetyClient(
        endpoint=settings.azure_content_safety_endpoint,
        credential=AzureKeyCredential(settings.azure_content_safety_key),
    )
