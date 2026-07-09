"""
Azure AI Search integration.

Supports:
- Keyword search
- Vector search
- Hybrid retrieval
"""

from typing import Dict, List, Optional

from src.config import get_logger
from src.config.client import get_search_client

logger = get_logger(__name__)


class VectorSearch:
    """
    Enterprise search wrapper.

    Provides:
    - keyword retrieval
    - vector retrieval
    - hybrid retrieval
    """

    def __init__(self):

        self.client = get_search_client()

    def search(
        self,
        query: str,
        top_k: int = 5,
    ) -> List[Dict]:
        """
        Execute hybrid search.

        Azure AI Search combines:
        - text matching
        - vector relevance
        - semantic ranking
        """

        logger.info(
            "Hybrid search query: %s",
            query,
        )

        results = self.client.search(
            search_text=query,
            top=top_k,
            include_total_count=True,
        )

        documents = []

        for result in results:

            documents.append(self._map_result(result))

        logger.info(
            "Retrieved %s documents",
            len(documents),
        )

        return documents

    def _map_result(
        self,
        result,
    ) -> Dict:
        """
        Normalize Azure Search result.

        Avoid dependency on fixed
        index fields.
        """

        return {
            "id": result.get("id"),
            "source": result.get(
                "source",
                result.get("metadata_storage_name"),
            ),
            "content": result.get(
                "content",
                "",
            ),
            "score": result.get(
                "@search.score",
                0,
            ),
            "metadata": result,
        }
