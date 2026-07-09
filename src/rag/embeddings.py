"""
Embedding generation.

Creates vector embeddings for
enterprise document chunks.
"""

from typing import List

from src.config import get_logger
from src.config.client import get_openai_client
from src.config.settings import get_settings

from src.rag.models import DocumentChunk

logger = get_logger(__name__)


class EmbeddingGenerator:
    """
    Generates embeddings using
    Azure AI Foundry OpenAI-compatible client.
    """

    def __init__(self):

        self.client = get_openai_client()

        self.settings = get_settings()

    def embed_chunks(
        self,
        chunks: List[DocumentChunk],
    ) -> List[dict]:
        """
        Generate embeddings for chunks.
        """

        results = []

        for chunk in chunks:

            embedding = self.client.embeddings.create(
                model=(self.settings.azure_openai_embedding_deployment),
                input=chunk.content,
            )

            vector = embedding.data[0].embedding

            results.append(
                {
                    "chunk_id": chunk.chunk_id,
                    "document_id": chunk.document_id,
                    "content": chunk.content,
                    "section": chunk.section,
                    "source": chunk.metadata.get("source"),
                    "title": chunk.metadata.get("title"),
                    "embedding": vector,
                }
            )

        logger.info(
            "Generated embeddings for %s chunks",
            len(results),
        )

        return results
