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
Agent response
"""

from typing import Dict, List

from src.config import get_logger

from src.rag.chunker import DocumentChunker
from src.rag.embeddings import EmbeddingGenerator
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
        document: Dict[str, str],
    ):
        """
        Process and store a document.
        """

        chunks = self.chunker.chunk_document(document)

        embedded_chunks = self.embeddings.embed_chunks(chunks)

        return self.search.upload_documents(embedded_chunks)

    def retrieve(
        self,
        query: str,
    ) -> List[Dict]:
        """
        Retrieve relevant enterprise context.
        """

        return self.search.search(query)

    def retrieve_context(
        self,
        query: str,
    ) -> str:
        """
        Retrieve and format enterprise context.
        """

        documents = self.retrieve(query)

        return self.build_context(documents)

    def build_context(
        self,
        documents: List[Dict],
    ) -> str:
        """
        Convert retrieved documents into
        model context.
        """

        return "\n\n".join([doc["content"] for doc in documents if doc.get("content")])
