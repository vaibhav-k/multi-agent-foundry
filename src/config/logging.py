"""
Application logging configuration.
"""

from __future__ import annotations

import logging
import sys

from src.config.settings import get_settings

LOG_FORMAT = "%(asctime)s | " "%(levelname)-8s | " "%(name)s | " "%(message)s"


def configure_logging() -> None:
    """
    Configure application logging.
    """

    settings = get_settings()

    logging.basicConfig(
        level=getattr(
            logging,
            settings.log_level.upper(),
            logging.INFO,
        ),
        format=LOG_FORMAT,
        handlers=[
            logging.StreamHandler(sys.stdout),
        ],
        force=True,
    )

    # Reduce dependency noise
    noisy_loggers = [
        "azure",
        "azure.identity",
        "azure.core",
        "httpx",
        "httpcore",
        "openai",
    ]

    for logger_name in noisy_loggers:
        logging.getLogger(logger_name).setLevel(logging.WARNING)


def get_logger(name: str) -> logging.Logger:
    """
    Return application logger.
    """
    return logging.getLogger(name)
