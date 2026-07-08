"""
Azure AI Search integration.

Handles:
- Vector document upload
- Similarity search
"""

from typing import Dict, List

from azure.search.documents import SearchClient
from azure.core.credentials import AzureKeyCredential

from src.config import get_logger, get_settings

logger = get_logger(__name__)


class VectorSearch:
    """
    Azure AI Search vector store wrapper.

    Future enhancements:
    - Hybrid search
    - Semantic ranking
    - Filters
    """

    def __init__(self):

        settings = get_settings()

        self.client = SearchClient(
            endpoint=settings.azure_search_endpoint,
            index_name=settings.azure_search_index,
            credential=AzureKeyCredential(settings.azure_search_key),
        )

    def upload_documents(
        self,
        documents: List[Dict],
    ):
        """
        Upload embedded documents.
        """

        result = self.client.upload_documents(documents)

        logger.info(
            "Uploaded %s documents",
            len(result),
        )

        return result

    def search(
        self,
        query: str,
        top_k: int = 5,
    ) -> List[Dict]:

        try:

            results = self.client.search(
                search_text=query,
                top=top_k,
            )

            documents = []

            for item in results:
                documents.append(
                    {
                        "content": item.get("content"),
                        "source": item.get("source"),
                    }
                )

            return documents

        except Exception as exc:

            logger.warning(
                "Azure Search unavailable: %s",
                exc,
            )

            return []
