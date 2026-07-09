"""
RAG Pipeline.

Responsible for enterprise document ingestion
and retrieval orchestration.

Ingestion Flow:

Enterprise Documents
        |
        v
Document Loader
        |
        v
Chunking
        |
        v
Embedding Generation
        |
        v
Azure AI Search Index


Retrieval Flow:

User Query
        |
        v
Azure AI Search
        |
        v
Retrieved Documents
"""

from typing import Dict, List

from src.config import get_logger

from src.rag.chunker import DocumentChunker
from src.rag.embeddings import EmbeddingGenerator
from src.rag.models import RAGDocument
from src.rag.search import VectorSearch

logger = get_logger(__name__)


class RAGPipeline:
    """
    Enterprise Retrieval Augmented Generation pipeline.

    Handles:

    - Document ingestion
    - Chunk creation
    - Embedding generation
    - Search indexing
    - Context construction
    """

    def __init__(
        self,
        chunker: DocumentChunker | None = None,
        embeddings: EmbeddingGenerator | None = None,
        search: VectorSearch | None = None,
    ):

        self.chunker = chunker if chunker else DocumentChunker()

        self.embeddings = embeddings if embeddings else EmbeddingGenerator()

        self.search = search if search else VectorSearch()

    # -------------------------------------------------
    # INGESTION
    # -------------------------------------------------

    def ingest_document(
        self,
        document: Dict[str, str],
    ) -> List[RAGDocument]:
        """
        Process one enterprise document.

        Steps:

        Document
            |
            v
        Chunking
            |
            v
        Embeddings
            |
            v
        Azure Search Upload
        """

        logger.info(
            "Ingesting document: %s",
            document.get("source"),
        )

        chunks = self.chunker.chunk_document(document)

        embedded_chunks = self.embeddings.embed_chunks(chunks)

        documents = []

        for chunk in embedded_chunks:

            rag_document = RAGDocument(
                document_id=chunk["chunk_id"],
                source=chunk.get("source"),
                title=chunk.get(
                    "title",
                    chunk.get("source"),
                ),
                content=chunk["content"],
                embedding=chunk.get("embedding"),
                metadata={"chunk_id": chunk["chunk_id"]},
            )

            documents.append(rag_document)

        self.search.upload_documents([document.model_dump() for document in documents])

        logger.info(
            "Indexed %s chunks",
            len(documents),
        )

        return documents

    # -------------------------------------------------
    # RETRIEVAL
    # -------------------------------------------------

    def retrieve(
        self,
        query: str,
        top_k: int = 5,
    ) -> List[RAGDocument]:
        """
        Retrieve enterprise documents.
        """

        return self.search.search(
            query=query,
            top_k=top_k,
        )

    def retrieve_context(
        self,
        query: str,
        top_k: int = 5,
    ) -> str:
        """
        Retrieve documents and build
        LLM context.
        """

        documents = self.retrieve(
            query=query,
            top_k=top_k,
        )

        return self.build_context(documents)

    # -------------------------------------------------
    # CONTEXT BUILDING
    # -------------------------------------------------

    def build_context(
        self,
        documents: List[RAGDocument],
    ) -> str:
        """
        Convert retrieved documents into
        LLM context.
        """

        context_parts = []

        for document in documents:

            context_parts.append(f"""
Source:
{document.source}


Content:
{document.content}
""")

        return "\n\n".join(context_parts)
