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
    """

    def __init__(self):

        self.search = VectorSearch()

    def retrieve(
        self,
        query: str,
        top_k: int = 5,
    ) -> List[Dict]:
        """
        Retrieve relevant documents.

        Returns:

        [
            {
                "content": "...",
                "source": "vpn.md",
                "title": "VPN Guide",
                "section": "Setup",
                "score": 0.91
            }
        ]
        """

        logger.info(
            "Retrieving documents for query: %s",
            query,
        )

        results = self.search.search(
            query,
            top_k,
        )

        logger.info(
            "Raw search results count: %s",
            len(results),
        )

        for result in results:
            logger.info(
                "Search result: %s",
                result,
            )

        logger.info(
            "Retriever returned %s documents",
            len(results),
        )

        logger.info(
            "Documents: %s",
            results,
        )

        documents = []

        for item in results:

            documents.append(
                {
                    "document_id": item.get("document_id"),
                    "content": item.get(
                        "content",
                        "",
                    ),
                    "source": item.get(
                        "source",
                    ),
                    "title": item.get(
                        "title",
                    ),
                    "section": item.get(
                        "section",
                    ),
                    "score": item.get(
                        "score",
                        0.0,
                    ),
                }
            )

        logger.info(
            "Retrieved %s documents",
            len(documents),
        )

        return documents


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
