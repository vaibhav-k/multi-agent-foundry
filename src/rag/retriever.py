"""
RAG Retriever.

Responsible for retrieving enterprise documents
from Azure AI Search.

Pipeline:

User Query
    |
Query Rewrite
    |
RAGRetriever
    |
Azure AI Search
    |
RAGDocument[]
    |
Document Reranker
    |
Knowledge Agent
"""

from typing import List

from src.config import get_logger

from src.rag.models import RAGDocument
from src.rag.search import VectorSearch

logger = get_logger(__name__)


class RAGRetriever:
    """
    Enterprise document retriever.

    Responsibilities:

    - Execute search queries
    - Retrieve relevant documents
    - Normalize search results
    - Provide documents for reranking
    """

    def __init__(
        self,
        search: VectorSearch | None = None,
    ):
        """
        Initialize retriever.

        Allows dependency injection
        for testing.
        """

        self.search = search if search else VectorSearch()

    def retrieve(
        self,
        query: str,
        top_k: int = 5,
    ) -> List[RAGDocument]:
        """
        Retrieve enterprise documents.

        Args:

            query:
                Search query after query rewriting.

            top_k:
                Number of documents to retrieve.


        Returns:

            List of RAGDocument objects.
        """

        logger.info(f"Retrieving documents for query: {query}")

        documents = self.search.search(
            query,
            top_k,
        )

        filtered_documents = [document for document in documents if document.content]

        logger.info(f"Retrieved {len(filtered_documents)} valid documents")

        return filtered_documents


class RAGBuilder:
    """
    Builds LLM context from retrieved documents.

    Converts RAGDocument objects into a grounded
    context block for the Knowledge Agent.
    """

    def __init__(
        self,
        max_documents: int = 5,
    ):
        self.max_documents = max_documents

    def build_context(
        self,
        documents: List[RAGDocument],
    ) -> str:
        """
        Convert RAGDocument objects into LLM context.

        Args:

            documents:
                List of RAGDocument objects.

        Returns:

            Formatted context string.
        """

        if not documents:

            return "No relevant enterprise " "documents found."

        context_parts = []

        for index, document in enumerate(
            documents[: self.max_documents],
            start=1,
        ):

            content = document.content or ""

            source = document.source or document.title or "unknown"

            score = document.score

            context_parts.append(f"""
Document {index}

Source:
{source}

Relevance Score:
{score}

Content:
{content}
""".strip())

        return "\n\n---\n\n".join(context_parts)
