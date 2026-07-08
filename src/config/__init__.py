"""
Configuration package.

Provides centralized access to application settings,
logging, and service clients.
"""

from .client import (
    get_content_safety_client,
    get_openai_client,
    get_project_client,
    get_search_client,
)

from .logging import (
    configure_logging,
    get_logger,
)

from .settings import (
    Settings,
    get_settings,
)

__all__ = [
    "Settings",
    "get_settings",
    "get_project_client",
    "get_openai_client",
    "get_search_client",
    "get_content_safety_client",
    "configure_logging",
    "get_logger",
]
