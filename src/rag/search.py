"""
Azure AI Search integration.
"""

from typing import List, Dict

from azure.search.documents import SearchClient

from azure.search.documents.models import VectorizedQuery

from src.config import get_logger
from src.config.client import get_search_client

logger = get_logger(__name__)


class VectorSearch:
    """
    Handles vector retrieval from Azure AI Search.
    """

    def __init__(self):

        self.client: SearchClient = get_search_client()

    def upload_documents(
        self,
        documents: List[Dict],
    ):
        """
        Upload indexed chunks.
        """

        return self.client.upload_documents(documents)

    def search(
        self,
        query: str,
        top_k: int = 5,
    ) -> List[Dict]:
        """
        Search enterprise documents.

        Returns normalized retrieval results.
        """

        logger.info(f"Searching Azure AI Search: {query}")

        results = self.client.search(
            search_text=query,
            top=top_k,
            select=[
                "content",
                "source",
                "chunk_id",
            ],
        )

        documents = []

        for result in results:

            documents.append(
                {
                    "chunk_id": result.get("chunk_id"),
                    "source": result.get("source"),
                    "content": result.get("content"),
                    "score": result.get(
                        "@search.score",
                        0.0,
                    ),
                }
            )

        return documents
