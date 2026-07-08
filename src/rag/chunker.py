"""
Document chunking utilities.

Responsible for splitting enterprise documents into
retrieval-friendly chunks while preserving metadata.
"""

from typing import Dict, List

from src.config import get_logger

logger = get_logger(__name__)


class DocumentChunker:
    """
    Splits documents into smaller chunks.

    Future enhancements:
    - Token based splitting
    - Semantic chunking
    - Overlap optimization
    """

    def __init__(
        self,
        chunk_size: int = 500,
        overlap: int = 50,
    ):
        self.chunk_size = chunk_size
        self.overlap = overlap

    def chunk_document(
        self,
        document: Dict[str, str],
    ) -> List[Dict[str, str]]:
        """
        Split a document into chunks.

        Input:
        {
            "source": "vpn.md",
            "content": "..."
        }

        Output:
        [
            {
                "chunk_id": "vpn.md-001",
                "source": "vpn.md",
                "content": "..."
            }
        ]
        """

        content = document["content"]
        source = document["source"]

        words = content.split()

        chunks = []

        start = 0
        chunk_number = 1

        while start < len(words):

            end = start + self.chunk_size

            chunk_words = words[start:end]

            chunks.append(
                {
                    "chunk_id": f"{source}-{chunk_number:03d}",
                    "source": source,
                    "content": " ".join(chunk_words),
                }
            )

            chunk_number += 1

            start = end - self.overlap

            if start < 0:
                start = 0

        logger.info(
            "Created %s chunks from %s",
            len(chunks),
            source,
        )

        return chunks
