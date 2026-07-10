"""
Embedding generation module.

Generates vector embeddings using Azure AI Foundry.

Flow:

Chunk
 |
 v
text-embedding-3-small
 |
 v
Chunk + embedding
"""

from typing import Dict, List

from src.config import get_logger
from src.config.client import get_embedding_client
from src.config.settings import get_settings

logger = get_logger(__name__)


class EmbeddingGenerator:
    """
    Generates embeddings for document chunks.
    """

    def __init__(self):
        self.client = get_embedding_client()

        settings = get_settings()

        self.model = settings.azure_openai_embedding_deployment

    def embed_text(
        self,
        text: str,
    ) -> List[float]:
        """
        Generate embedding vector.
        """

        response = self.client.embed(input=[text])

        return response.data[0].embedding

    def embed_chunks(
        self,
        chunks: List[Dict],
    ) -> List[Dict]:
        """
        Add embeddings to chunks.
        """

        results = []

        logger.info(
            "Generating embeddings for %s chunks",
            len(chunks),
        )

        for chunk in chunks:

            embedding = self.embed_text(chunk["content"])

            results.append(
                {
                    **chunk,
                    "embedding": embedding,
                }
            )

        return results
