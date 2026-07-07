"""
Configuration package.

Exports application settings and client helpers.
"""

from .client import get_client
from .settings import (
    CHAT_DEPLOYMENT,
    EMBEDDING_DEPLOYMENT,
    FOUNDRY_API_KEY,
    FOUNDRY_ENDPOINT,
)

__all__ = [
    "CHAT_DEPLOYMENT",
    "EMBEDDING_DEPLOYMENT",
    "FOUNDRY_API_KEY",
    "FOUNDRY_ENDPOINT",
    "get_client",
]
