"""
Enterprise document retrieval.

Retrieves relevant knowledge chunks
from Azure AI Search.
"""

from typing import Any, List, Dict

from src.config import get_logger
from src.rag.search import VectorSearch

logger = get_logger(__name__)


class RAGRetriever:
    """
    Retrieves enterprise knowledge documents.

    Pipeline:

    Query
      |
      v
    Azure AI Search
      |
      v
    Normalized Documents
    """

    def __init__(
        self,
        top_k: int = 5,
    ):

        self.search = VectorSearch()

        self.top_k = top_k

    def retrieve(
        self,
        query: str,
        top_k: int | None = None,
    ) -> List[Dict]:
        """
        Retrieve relevant enterprise documents.

        Args:

            query:
                Search query.

            top_k:
                Override default result count.

        Returns:

            List of normalized documents.
        """

        limit = top_k if top_k else self.top_k

        logger.info(
            "Retrieving documents. query=%s top_k=%s",
            query,
            limit,
        )

        documents = self.search.search(
            query=query,
            top_k=limit,
        )

        if not documents:

            logger.warning(
                "No documents found for query=%s",
                query,
            )

            return []

        logger.info(
            "Retrieved %s documents",
            len(documents),
        )

        return self._normalize(documents)

    def _normalize(
        self,
        documents: List[Dict],
    ) -> List[Dict]:
        """
        Ensure every document has
        required RAG fields.
        """

        normalized = []

        for document in documents:

            normalized.append(
                {
                    "id": document.get("id"),
                    "source": document.get(
                        "source",
                        "unknown",
                    ),
                    "content": document.get(
                        "content",
                        "",
                    ),
                    "score": document.get(
                        "score",
                        0,
                    ),
                    "metadata": document.get(
                        "metadata",
                        {},
                    ),
                }
            )

        return normalized


class RAGBuilder:
    """
    Builds LLM context from retrieved documents.

    Converts search results into a grounded context block
    that can be passed to an agent.
    """

    def __init__(
        self,
        max_documents: int = 5,
    ):
        self.max_documents = max_documents

    def build_context(
        self,
        documents: List[Dict[str, Any]],
    ) -> str:
        """
        Convert retrieved documents into context text.

        Expected document format:

        {
            "content": "...",
            "source": "document.pdf"
        }

        Returns:
            Formatted context string.
        """

        if not documents:
            return "No relevant enterprise documents found."

        context_parts = []

        for index, document in enumerate(
            documents[: self.max_documents],
            start=1,
        ):
            content = document.get(
                "content",
                "",
            )

            source = document.get(
                "source",
                "unknown",
            )

            context_parts.append(f"""
Document {index}
Source: {source}

{content}
""".strip())

        return "\n\n---\n\n".join(context_parts)
