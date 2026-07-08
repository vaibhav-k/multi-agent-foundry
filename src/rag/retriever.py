"""
RAG retriever.

Responsible for retrieving enterprise knowledge
from Azure AI Search.
"""

from typing import Any, List, Dict

from src.config import get_logger
from src.rag.search import VectorSearch

logger = get_logger(__name__)


class RAGRetriever:
    """
    Enterprise knowledge retriever.
    """

    def __init__(self):
        self.search = VectorSearch()

    def retrieve(
        self,
        query: str,
        top_k: int = 3,
    ) -> List[Dict]:

        logger.info(f"Retrieving documents for query: {query}")

        results = self.search.search(
            query=query,
            top_k=top_k,
        )

        return results


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
