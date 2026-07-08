"""
Application logging configuration.
"""

import logging
import sys

LOG_FORMAT = "%(asctime)s | " "%(levelname)-8s | " "%(name)s | " "%(message)s"


def configure_logging(level: int = logging.INFO) -> None:
    """
    Configure application logging.
    """

    logging.basicConfig(
        level=level,
        format=LOG_FORMAT,
        handlers=[
            logging.StreamHandler(sys.stdout),
        ],
        force=True,
    )


def get_logger(name: str) -> logging.Logger:
    """
    Returns a configured logger.
    """

    return logging.getLogger(name)
