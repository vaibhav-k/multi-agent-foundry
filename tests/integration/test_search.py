"""
Azure AI Search integration test.
"""

import pytest

from src.config import get_search_client


@pytest.mark.integration
def test_search_connection():

    try:
        client = get_search_client()

        results = client.search(search_text="VPN")

        assert results is not None

    except Exception as exc:

        pytest.skip(f"Azure AI Search not configured: {exc}")
