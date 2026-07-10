"""
Application settings.

Loads configuration from environment variables and the .env file.
"""

from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application configuration."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # ==========================================================
    # Application
    # ==========================================================

    log_level: str = Field(
        default="INFO",
        alias="LOG_LEVEL",
    )

    # ==========================================================
    # Azure AI Foundry Project
    # ==========================================================

    azure_ai_project_endpoint: str = Field(
        ...,
        alias="AZURE_AI_PROJECT_ENDPOINT",
    )

    # ==========================================================
    # Model Deployments
    # ==========================================================

    # Deployment names configured in:
    # Azure AI Foundry
    # -> Project
    # -> Models + Endpoints
    # -> Deployments

    azure_openai_chat_deployment: str = Field(
        ...,
        alias="AZURE_OPENAI_CHAT_DEPLOYMENT",
    )

    azure_openai_embedding_deployment: str = Field(
        ...,
        alias="AZURE_OPENAI_EMBEDDING_DEPLOYMENT",
    )

    azure_inference_endpoint: str
    azure_inference_key: str

    azure_openai_embedding_deployment: str = "text-embedding-3-small"

    # ==========================================================
    # Azure AI Search
    # ==========================================================

    azure_search_endpoint: str = Field(
        ...,
        alias="AZURE_SEARCH_ENDPOINT",
    )

    azure_search_key: str = Field(
        ...,
        alias="AZURE_SEARCH_KEY",
    )

    azure_search_index: str = Field(
        default="enterprise-documents",
        alias="AZURE_SEARCH_INDEX",
    )

    # ==========================================================
    # Azure AI Content Safety
    # ==========================================================

    azure_content_safety_endpoint: str = Field(
        ...,
        alias="AZURE_CONTENT_SAFETY_ENDPOINT",
    )

    azure_content_safety_key: str = Field(
        ...,
        alias="AZURE_CONTENT_SAFETY_KEY",
    )


@lru_cache
def get_settings() -> Settings:
    """Return cached application settings."""
    return Settings()
