"""
Document chunking module.

Splits enterprise documents into smaller
retrieval-friendly chunks.
"""

from typing import List, Dict

from src.config import get_logger

logger = get_logger(__name__)


class DocumentChunker:
    """
    Creates chunks from loaded documents.

    Future enhancements:
    - Token based splitting
    - Semantic chunking
    - Azure AI Document Intelligence
    """

    def __init__(
        self,
        chunk_size: int = 500,
        overlap: int = 50,
    ):
        """
        Args:
            chunk_size:
                Number of characters per chunk.

            overlap:
                Characters repeated between chunks.
        """

        self.chunk_size = chunk_size
        self.overlap = overlap

    def chunk_documents(
        self,
        documents: List[Dict[str, str]],
    ) -> List[Dict[str, str]]:
        """
        Split documents into chunks.

        Input:

        [
            {
                "content": "...",
                "source": "vpn.md"
            }
        ]


        Output:

        [
            {
                "content": "...",
                "source": "vpn.md",
                "chunk_id": "vpn.md_0"
            }
        ]
        """

        chunks = []

        for document in documents:

            content = document["content"]

            source = document["source"]

            start = 0

            chunk_number = 0

            while start < len(content):

                end = start + self.chunk_size

                chunk_text = content[start:end]

                chunks.append(
                    {
                        "content": chunk_text,
                        "source": source,
                        "chunk_id": f"{source}_{chunk_number}",
                    }
                )

                chunk_number += 1

                start = end - self.overlap

                if start < 0:
                    start = 0

        logger.info(
            "Created %s chunks",
            len(chunks),
        )

        return chunks
