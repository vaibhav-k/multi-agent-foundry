"""
Enterprise document ingestion pipeline.

Flow:

Documents
    |
Chunking
    |
Embedding generation
    |
Azure AI Search upload
"""

from src.config import get_logger

from src.rag.documents import DocumentLoader
from src.rag.chunker import DocumentChunker
from src.rag.embeddings import EmbeddingGenerator
from src.rag.search import VectorSearch

logger = get_logger(__name__)


class DocumentIngestion:
    """
    End-to-end document ingestion.
    """

    def __init__(self):

        self.loader = DocumentLoader()

        self.chunker = DocumentChunker()

        self.embedding = EmbeddingGenerator()

        self.search = VectorSearch()

    def run(self):
        """
        Execute ingestion workflow.
        """

        documents = self.loader.load_documents()

        chunks = self.chunker.chunk_documents(documents)

        embedded_chunks = self.embedding.embed_chunks(chunks)

        result = self.search.upload_documents(embedded_chunks)

        return result
