"""
Azure AI Search integration.

Responsibilities:

- Execute enterprise document search
- Support hybrid retrieval
- Map Azure Search results into RAGDocument
"""

from typing import List

from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient

from src.config import get_logger
from src.config.settings import get_settings
from src.rag.models import RAGDocument

logger = get_logger(__name__)


class VectorSearch:
    """
    Azure AI Search wrapper.

    Converts Azure Search documents into
    internal RAGDocument objects.
    """

    def __init__(
        self,
        client: SearchClient | None = None,
    ):

        settings = get_settings()

        self.client = (
            client
            if client
            else SearchClient(
                endpoint=settings.azure_search_endpoint,
                index_name=settings.azure_search_index,
                credential=AzureKeyCredential(settings.azure_search_key),
            )
        )

    def search(
        self,
        query: str,
        top_k: int = 5,
    ) -> List[RAGDocument]:
        """
        Execute enterprise document search.

        Current mode:
        - Text search

        Ready for:
        - Vector search
        - Hybrid search
        - Semantic ranking
        """

        logger.info(f"Search query: {query}")

        results = self.client.search(
            search_text=query,
            top=top_k,
            include_total_count=True,
        )

        documents = []

        for result in results:

            document = self._map_result(result)

            if document:

                documents.append(document)

        logger.info(f"Retrieved {len(documents)} documents")

        return documents

    def _map_result(
        self,
        result: dict,
    ) -> RAGDocument | None:
        """
        Convert Azure Search result into
        RAGDocument.
        """

        content = result.get("content") or result.get("text")

        if not content:

            logger.warning("Skipping result without content")

            return None

        document_id = (
            result.get("document_id") or result.get("chunk_id") or result.get("id") or "unknown"
        )

        source = result.get("source") or result.get("file_name")

        title = result.get("title") or source

        score = result.get("@search.score")

        return RAGDocument(
            document_id=document_id,
            source=source,
            title=title,
            content=content,
            score=score,
            metadata={
                "search_score": score,
            },
        )

    def upload_documents(
        self,
        documents: list[dict],
    ):

        normalized = []

        for doc in documents:

            normalized.append(
                {
                    "chunk_id": doc["chunk_id"],
                    "content": doc["content"],
                    "source": doc.get("source", ""),
                    "embedding": doc["embedding"],
                }
            )

        return self.client.upload_documents(documents=normalized)
