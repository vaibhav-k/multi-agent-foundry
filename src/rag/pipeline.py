"""
RAG pipeline orchestration.

Enterprise Retrieval-Augmented Generation pipeline.

Ingestion Flow:

Document
    |
Document Chunking
    |
Embedding Generation
    |
Azure AI Search Index
    |
Stored Knowledge Base


Retrieval Flow:

User Query
    |
Query Optimization
    |
Azure AI Search
    |
Retrieved Documents
    |
Context Builder
    |
Knowledge Agent
    |
Grounded Response
"""

from typing import Dict, List

from src.config import get_logger

from src.rag.chunker import DocumentChunker
from src.rag.embeddings import EmbeddingGenerator
from src.rag.search import VectorSearch

logger = get_logger(__name__)


class RAGPipeline:
    """
    Enterprise Retrieval-Augmented Generation pipeline.

    Responsible for:

    - Document ingestion
    - Chunk generation
    - Embedding creation
    - Search indexing
    - Enterprise document retrieval
    - Context construction
    """

    def __init__(self):

        self.chunker = DocumentChunker()

        self.embeddings = EmbeddingGenerator()

        self.search = VectorSearch()

    # ------------------------------------------------------------------
    # Ingestion
    # ------------------------------------------------------------------

    def ingest_document(
        self,
        document: Dict[str, str],
    ):
        """
        Process and store an enterprise document.

        Steps:

        1. Split document into chunks
        2. Generate embeddings
        3. Upload vectors to Azure AI Search
        """

        logger.info("Starting document ingestion")

        chunks = self.chunker.chunk_document(document)

        logger.info(
            "Generated %s chunks",
            len(chunks),
        )

        embedded_chunks = self.embeddings.embed_chunks(chunks)

        result = self.search.upload_documents(embedded_chunks)

        logger.info("Document ingestion completed")

        return result

    # ------------------------------------------------------------------
    # Retrieval
    # ------------------------------------------------------------------

    def retrieve(
        self,
        query: str,
    ) -> List[Dict]:
        """
        Retrieve relevant enterprise documents.

        Returns normalized search results
        for downstream agents.
        """

        logger.info(
            "Retrieving documents for query: %s",
            query,
        )

        documents = self.search.search(query)

        return [self.normalize_document(doc) for doc in documents]

    def retrieve_context(
        self,
        query: str,
    ) -> str:
        """
        Retrieve documents and build LLM context.
        """

        documents = self.retrieve(query)

        return self.build_context(documents)

    # ------------------------------------------------------------------
    # Context Construction
    # ------------------------------------------------------------------

    def build_context(
        self,
        documents: List[Dict],
    ) -> str:
        """
        Convert retrieved documents into
        grounded model context.

        Includes metadata to improve
        citation quality.
        """

        if not documents:
            return ""

        context_blocks = []

        for document in documents:

            content = document.get("content")

            if not content:
                continue

            source = document.get(
                "source",
                "unknown",
            )

            section = document.get(
                "section",
                "",
            )

            block = f"""
Source:
{source}

Section:
{section}

Content:
{content}
"""

            context_blocks.append(block.strip())

        return "\n\n---\n\n".join(context_blocks)

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def normalize_document(
        self,
        document: Dict,
    ) -> Dict:
        """
        Normalize Azure AI Search output.

        Ensures downstream agents receive
        a predictable structure.
        """

        return {
            "document_id": document.get(
                "id",
                document.get("document_id"),
            ),
            "title": document.get(
                "title",
                "",
            ),
            "content": document.get(
                "content",
                "",
            ),
            "source": document.get(
                "source",
                document.get(
                    "title",
                    "unknown",
                ),
            ),
            "section": document.get(
                "section",
            ),
            "score": document.get(
                "score",
                0.0,
            ),
        }
