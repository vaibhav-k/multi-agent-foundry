"""
Enterprise document chunking module.

Creates semantic chunks from enterprise documents.

Pipeline:

Document
    |
    v
Markdown Section Detection
    |
    v
Semantic Chunking
    |
    v
Metadata Enrichment
    |
    v
Azure AI Search Documents
"""

import re
from typing import Dict, List

from src.config import get_logger

logger = get_logger(__name__)


class DocumentChunker:
    """
    Enterprise semantic document chunker.

    Features:

    - Markdown heading detection
    - Section preservation
    - Configurable chunk size
    - Azure AI Search compatible IDs
    - Metadata enrichment
    """

    def __init__(
        self,
        chunk_size: int = 500,
    ):
        self.chunk_size = chunk_size

    def chunk_documents(
        self,
        documents: List[Dict[str, str]],
    ) -> List[Dict[str, str]]:
        """
        Chunk multiple enterprise documents.

        Input:

        [
            {
                "source": "vpn.md",
                "content": "..."
            }
        ]

        Output:

        [
            {
                "chunk_id": "...",
                "source": "...",
                "section": "...",
                "content": "..."
            }
        ]
        """

        chunks = []

        for document in documents:

            chunks.extend(self.chunk_document(document))

        logger.info(
            "Created %s document chunks",
            len(chunks),
        )

        return chunks

    def chunk_document(
        self,
        document: Dict[str, str],
    ) -> List[Dict[str, str]]:
        """
        Chunk a single document.
        """

        source = document["source"]

        content = document["content"]

        sections = self._split_markdown_sections(content)

        chunks = []

        chunk_number = 1

        for section in sections:

            section_title = section["title"]

            section_content = section["content"]

            section_chunks = self._split_content(section_content)

            for chunk_text in section_chunks:

                chunks.append(
                    {
                        "chunk_id": self._create_id(
                            source,
                            chunk_number,
                        ),
                        "source": source,
                        "title": source.replace(
                            ".md",
                            "",
                        ),
                        "section": section_title,
                        "content": chunk_text,
                    }
                )

                chunk_number += 1

        return chunks

    def _split_markdown_sections(
        self,
        content: str,
    ) -> List[Dict[str, str]]:
        """
        Split markdown documents by headings.

        Example:

        # VPN Setup

        Install VPN client

        becomes:

        {
          title:
          VPN Setup,

          content:
          Install VPN client
        }
        """

        matches = re.split(
            r"\n(?=#)",
            content,
        )

        sections = []

        for block in matches:

            block = block.strip()

            if not block:
                continue

            lines = block.splitlines()

            title = "General"

            if lines[0].startswith("#"):

                title = (
                    lines[0]
                    .replace(
                        "#",
                        "",
                    )
                    .strip()
                )

                body = "\n".join(lines[1:]).strip()

            else:

                body = block

            sections.append(
                {
                    "title": title,
                    "content": body,
                }
            )

        return sections

    def _split_content(
        self,
        content: str,
    ) -> List[str]:
        """
        Split section content into chunks.

        Uses word boundaries.
        """

        words = content.split()

        chunks = []

        for index in range(
            0,
            len(words),
            self.chunk_size,
        ):

            chunk_words = words[index : index + self.chunk_size]

            chunks.append(" ".join(chunk_words))

        return chunks

    def _create_id(
        self,
        source: str,
        number: int,
    ) -> str:
        """
        Create Azure Search compatible ID.
        """

        safe_source = re.sub(
            r"[^a-zA-Z0-9_-]",
            "_",
            source,
        )

        return f"{safe_source}" f"-chunk-{number}"
