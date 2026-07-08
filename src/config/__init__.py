"""
Configuration package.
"""

from .settings import get_settings

from .client import (
    get_project_client,
    get_openai_client,
    get_embedding_client,
)

from .logging import get_logger

__all__ = [
    "get_settings",
    "get_project_client",
    "get_openai_client",
    "get_embedding_client",
    "get_logger",
]
