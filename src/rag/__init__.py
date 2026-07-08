"""
Retrieval Augmented Generation (RAG) package.

Contains:
- document loading
- chunking
- embeddings
- vector search
- retrieval pipeline
"""

from .chunker import DocumentChunker
from .embeddings import EmbeddingGenerator
from .search import VectorSearch
from .pipeline import RAGPipeline

__all__ = [
    "DocumentChunker",
    "EmbeddingGenerator",
    "VectorSearch",
    "RAGPipeline",
]
