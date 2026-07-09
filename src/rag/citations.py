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

        for document in documents:

            if isinstance(document, dict):

                citations.append(
                    DocumentReference(
                        name=document.get(
                            "source",
                            "unknown",
                        ),
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

            citations.append(
                DocumentReference(
                    document_id=document.document_id,
                    name=(document.source or document.title or "unknown"),
                    section=section,
                    score=document.score,
                )
            )

        return citations
