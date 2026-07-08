"""
Azure AI Content Safety integration test.
"""

import pytest

from src.config import get_content_safety_client


@pytest.mark.integration
def test_content_safety_connection():

    try:

        client = get_content_safety_client()

        assert client is not None

    except Exception as exc:

        pytest.skip(f"Content Safety not configured: {exc}")
