"""
Citation generation utilities.

Creates references for grounded responses.
"""

from src.models import DocumentReference
from src.rag.models import RAGDocument


class CitationBuilder:
    """
    Builds document citations.

    Supports:
    - RAGDocument objects
    - Legacy dictionary documents
    """

    def build(
        self,
        documents: list[RAGDocument | dict],
    ) -> list[DocumentReference]:

        citations = []
        seen_sources = set()

        for document in documents:

            if isinstance(document, dict):

                name = document.get(
                    "source",
                    "unknown",
                )

                if name in seen_sources:
                    continue

                seen_sources.add(name)

                citations.append(
                    DocumentReference(
                        name=name,
                        section=document.get("section"),
                        score=document.get("score"),
                    )
                )

                continue

            section = None

            if document.metadata:
                section = getattr(
                    document.metadata,
                    "section",
                    None,
                )

            name = document.source or document.title or "unknown"

            if name in seen_sources:
                continue

            seen_sources.add(name)

            citations.append(
                DocumentReference(
                    document_id=document.document_id,
                    name=name,
                    section=section,
                    score=document.score,
                )
            )

        return citations
