"""
Client factory.

Creates reusable Azure AI Foundry and Azure OpenAI clients.
"""

from functools import lru_cache

from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from openai import AzureOpenAI

from src.config.settings import get_settings


@lru_cache
def get_project_client():

    settings = get_settings()

    return AIProjectClient(
        endpoint=settings.azure_ai_project_endpoint,
        credential=DefaultAzureCredential(),
    )


@lru_cache
def get_openai_client():
    """
    Azure AI Foundry OpenAI client.

    Used for:
    - Responses API
    - Agent workflows
    - gpt-5.4-mini
    """

    project_client = get_project_client()

    return project_client.get_openai_client()


@lru_cache
def get_embedding_client():
    """
    Azure OpenAI client.

    Used for:
    - text-embedding-3-small
    """

    settings = get_settings()

    return AzureOpenAI(
        azure_endpoint=settings.azure_ai_model_endpoint,
        api_key=settings.azure_ai_model_key,
        api_version="2024-05-01-preview",
    )
