"""
Shared pytest fixtures.

Fixtures defined here are available to all tests.
"""

import pytest

from src.config import get_settings


@pytest.fixture(scope="session")
def settings():
    """
    Provides application settings.
    """

    return get_settings()


@pytest.fixture
def sample_question():
    """
    Common test question.
    """

    return "How do I connect to the company VPN?"


@pytest.fixture
def sample_documents():
    """
    Mock enterprise documents for testing.
    """

    return [
        {
            "title": "VPN User Guide",
            "content": (
                "To connect to the company VPN, install the VPN client "
                "and authenticate using your company credentials."
            ),
        },
        {
            "title": "Password Policy",
            "content": ("Passwords must meet company security requirements."),
        },
    ]
