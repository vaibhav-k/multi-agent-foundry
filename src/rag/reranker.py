"""
Enterprise document reranking.

Improves retrieval quality by combining:

- search relevance score
- keyword matching
- metadata relevance

Pipeline:

Azure AI Search Results
          |
          v
Document Reranker
          |
          v
Top Relevant Documents
"""

from typing import Dict

from src.config import get_logger
from src.rag.models import RAGDocument

logger = get_logger(__name__)


class DocumentReranker:
    """
    Enterprise reranking component.

    Keeps retrieval candidates and reorders them based on relevance.
    """

    def __init__(
        self,
        top_k: int = 5,
    ):

        self.top_k = top_k

    def rerank(
        self,
        query: str,
        documents: list[RAGDocument | dict],
    ) -> list:
        """
        Reranks retrieved documents.

        Supports:
        - RAGDocument objects
        - Legacy dictionaries
        """

        if not documents:
            return []

        query_terms = set(query.lower().split())

        scored_documents = []

        for document in documents:

            if isinstance(document, dict):

                content = document.get(
                    "content",
                    "",
                ).lower()

                score = document.get(
                    "score",
                    0,
                )

                keyword_score = sum(1 for term in query_terms if term in content)

                document["score"] = score + keyword_score

                scored_documents.append(document)

                continue

            content = document.content.lower() if document.content else ""

            keyword_score = sum(1 for term in query_terms if term in content)

            existing_score = document.score or 0

            document.score = existing_score + keyword_score

            scored_documents.append(document)

        return sorted(
            scored_documents,
            key=lambda x: (x.score if hasattr(x, "score") else x.get("score", 0)),
            reverse=True,
        )

    def calculate_score(
        self,
        query_terms: set,
        document: Dict,
    ) -> float:
        """
        Calculate enterprise relevance score.

        Formula:

        Search score       50%
        Keyword match      30%
        Metadata match     20%
        """

        search_score = document.get(
            "score",
            0,
        )

        content = str(
            document.get(
                "content",
                "",
            )
        ).lower()

        title = str(
            document.get(
                "title",
                "",
            )
        ).lower()

        category = str(
            document.get(
                "category",
                "",
            )
        ).lower()

        text = content + " " + title + " " + category

        keyword_matches = sum(1 for term in query_terms if term in text)

        keyword_score = keyword_matches / max(len(query_terms), 1)

        metadata_score = 0.0

        if any(term in title for term in query_terms):
            metadata_score += 0.5

        if any(term in category for term in query_terms):
            metadata_score += 0.5

        final_score = (
            (search_score * 0.5) + (keyword_score * 0.3) + (metadata_score * 0.2)
        )

        return round(
            final_score,
            4,
        )
