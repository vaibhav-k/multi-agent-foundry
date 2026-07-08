"""
Embedding generation module.

Uses Azure OpenAI embedding deployment
to convert text into vector representations.
"""

from typing import List, Dict

from src.config import (
    get_logger,
    get_embedding_client,
    get_settings,
)

logger = get_logger(__name__)


class EmbeddingGenerator:
    """
    Generates embeddings for document chunks.

    Uses:
    Azure OpenAI
    text-embedding-3-small
    """

    def __init__(self):

        self.client = get_embedding_client()

        self.settings = get_settings()

    def generate_embedding(
        self,
        text: str,
    ) -> List[float]:
        """
        Generate vector embedding for text.
        """

        response = self.client.embeddings.create(
            model=(self.settings.azure_openai_embedding_deployment),
            input=text,
        )

        return response.data[0].embedding

    def embed_chunks(
        self,
        chunks: List[Dict[str, str]],
    ) -> List[Dict]:
        """
        Add embeddings to chunks.

        Input:

        {
            "content": "...",
            "source": "vpn.md"
        }


        Output:

        {
            "content": "...",
            "source": "vpn.md",
            "embedding": [...]
        }
        """

        embedded_chunks = []

        for chunk in chunks:

            logger.info(
                "Generating embedding for %s",
                chunk["chunk_id"],
            )

            vector = self.generate_embedding(chunk["content"])

            embedded_chunks.append(
                {
                    **chunk,
                    "embedding": vector,
                }
            )

        logger.info(
            "Generated embeddings for %s chunks",
            len(embedded_chunks),
        )

        return embedded_chunks
