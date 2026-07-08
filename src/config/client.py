"""
Client factory.

Creates reusable Azure clients used throughout the application.
"""

from functools import lru_cache

from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from azure.search.documents import SearchClient
from azure.core.credentials import AzureKeyCredential
from azure.ai.contentsafety import ContentSafetyClient
from azure.identity import get_bearer_token_provider

import openai

from src.config.settings import get_settings


@lru_cache
def get_project_client():
    """
    Creates and returns an Azure AI Foundry project client.

    The project client provides access to Azure AI Foundry project
    resources and services using Microsoft Entra ID authentication.

    Returns:
        AIProjectClient: Authenticated Azure AI Foundry project client.
    """
    settings = get_settings()

    return AIProjectClient(
        endpoint=settings.azure_ai_project_endpoint,
        credential=DefaultAzureCredential(),
    )


def get_openai_client():
    """
    Creates and returns an OpenAI-compatible client for Azure AI Foundry models.

    Uses the Azure AI Foundry OpenAI-compatible endpoint with Microsoft Entra ID
    authentication. The returned client can be used with standard OpenAI SDK
    interfaces such as chat completions and responses APIs.

    Returns:
        openai.OpenAI: Authenticated OpenAI-compatible client configured for
        Azure AI Foundry model inference.
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


@lru_cache
def get_embedding_client():
    """
    Creates and returns an Azure OpenAI client for embedding generation.

    This client connects to the Azure OpenAI resource configured for embedding
    models and uses API key authentication.

    Returns:
        AzureOpenAI: Authenticated Azure OpenAI client for embedding operations.
    """
    settings = get_settings()

    # Keeping this if your embedding model is a standard Azure OpenAI resource instance
    from openai import AzureOpenAI

    return AzureOpenAI(
        azure_endpoint=settings.azure_openai_embedding_endpoint,
        api_version="2025-04-01-preview",
        api_key=settings.azure_openai_embedding_key,
    )


@lru_cache
def get_search_client():
    """
    Creates and returns an Azure AI Search client.

    The client provides access to the configured search index for document
    retrieval and vector or keyword-based search operations.

    Returns:
        SearchClient: Authenticated Azure AI Search client.
    """
    settings = get_settings()

    return SearchClient(
        endpoint=settings.azure_search_endpoint,
        index_name=settings.azure_search_index,
        credential=AzureKeyCredential(settings.azure_search_key),
    )


@lru_cache
def get_content_safety_client():
    """
    Creates and returns an Azure AI Content Safety client.

    The client is used to analyze and evaluate content using Azure AI Content
    Safety APIs.

    Returns:
        ContentSafetyClient: Authenticated Azure AI Content Safety client.
    """
    settings = get_settings()

    return ContentSafetyClient(
        endpoint=settings.azure_content_safety_endpoint,
        credential=AzureKeyCredential(settings.azure_content_safety_key),
    )
