"""
Configuration package.
"""

from .client import (
    get_credential,
    get_project_client,
    get_openai_client,
    get_embedding_client,
    get_search_client,
    get_content_safety_client,
)

from .settings import get_settings

from .logging import configure_logging, get_logger

__all__ = [
    "configure_logging",
    "get_credential",
    "get_settings",
    "get_project_client",
    "get_openai_client",
    "get_embedding_client",
    "get_search_client",
    "get_content_safety_client",
    "get_logger",
]
