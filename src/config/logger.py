"""
Application logging configuration.
"""

import logging

from src.config.settings import get_settings


def get_logger(name: str) -> logging.Logger:
    """
    Create application logger.
    """

    settings = get_settings()

    logging.basicConfig(
        level=settings.log_level,
        format=("%(asctime)s | " "%(levelname)s | " "%(name)s | " "%(message)s"),
    )

    return logging.getLogger(name)
