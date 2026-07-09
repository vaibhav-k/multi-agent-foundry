"""
RAG pipeline orchestration.

Flow:

Document
   |
Chunking
   |
Embedding
   |
Azure AI Search
   |
Retrieval
   |
Knowledge Agent
"""

from typing import List

from src.config import get_logger

from src.rag.chunker import DocumentChunker
from src.rag.embeddings import EmbeddingGenerator
from src.rag.models import Document, DocumentChunk
from src.rag.search import VectorSearch

logger = get_logger(__name__)


class RAGPipeline:
    """
    Enterprise Retrieval Augmented Generation pipeline.
    """

    def __init__(self):

        self.chunker = DocumentChunker()

        self.embeddings = EmbeddingGenerator()

        self.search = VectorSearch()

    def ingest_document(
        self,
        document: Document,
    ):
        """
        Process and index an enterprise document.
        """

        logger.info(
            "Processing document %s",
            document.document_id,
        )

        chunks = self.chunker.chunk_documents([document])

        embedded_chunks = self.embeddings.embed_chunks(chunks)

        return self.search.upload_documents(embedded_chunks)

    def ingest_documents(
        self,
        documents: List[Document],
    ):
        """
        Process multiple documents.
        """

        results = []

        for document in documents:

            results.append(self.ingest_document(document))

        return results

    def retrieve(
        self,
        query: str,
    ) -> List[dict]:
        """
        Retrieve relevant enterprise chunks.
        """

        return self.search.search(query)

    def retrieve_context(
        self,
        query: str,
    ) -> str:
        """
        Retrieve and format context.
        """

        documents = self.retrieve(query)

        return self.build_context(documents)

    def build_context(
        self,
        documents: List[dict],
    ) -> str:
        """
        Convert retrieved chunks into
        LLM context.
        """

        context = []

        for document in documents:

            content = document.get("content")

            source = document.get("source")

            if content:

                context.append(f"""
Source:
{source}

Content:
{content}
""")

        return "\n\n".join(context)
