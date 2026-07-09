"""
Embedding generation module.

Responsible for generating vector embeddings
for document chunks.

Flow:

Document Chunk
        |
        v
Embedding Model
        |
        v
Chunk + Embedding Vector
"""

from typing import Dict, List

from src.config import get_logger
from src.config.client import get_embedding_client

logger = get_logger(__name__)


class EmbeddingGenerator:
    """
    Generates embeddings for RAG documents.

    Responsibilities:

    - Generate vector embeddings
    - Attach vectors to chunks
    - Return Azure AI Search compatible data
    """

    def __init__(
        self,
        client=None,
        deployment_name: str | None = None,
    ):
        """
        Initialize embedding client.

        Dependency injection is supported
        for testing.
        """

        self.client = client if client else get_embedding_client()

        self.deployment_name = deployment_name

    def embed_text(
        self,
        text: str,
    ) -> List[float]:
        """
        Generate embedding for text.
        """

        logger.debug("Generating embedding")

        response = self.client.embeddings.create(
            model=self.deployment_name,
            input=text,
        )

        return response.data[0].embedding

    def embed_chunks(
        self,
        chunks: List[Dict[str, str]],
    ) -> List[Dict]:
        """
        Generate embeddings for document chunks.

        Input:

        [
            {
                "chunk_id": "vpn-1",
                "source": "vpn.md",
                "content": "..."
            }
        ]


        Output:

        [
            {
                "chunk_id": "vpn-1",
                "source": "vpn.md",
                "content": "...",
                "embedding": [...]
            }
        ]
        """

        embedded_chunks = []

        logger.info(
            "Embedding %s chunks",
            len(chunks),
        )

        for chunk in chunks:

            embedding = self.embed_text(chunk["content"])

            embedded_chunk = {
                **chunk,
                "embedding": embedding,
            }

            embedded_chunks.append(embedded_chunk)

        logger.info(
            "Generated embeddings for %s chunks",
            len(embedded_chunks),
        )

        return embedded_chunks
