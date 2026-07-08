"""
Retrieval Augmented Generation (RAG) package.

Components:
- Document loading
- Text chunking
- Embeddings generation
- Vector search
- Context retrieval
"""

from .loader import DocumentLoader
from .chunker import DocumentChunker
from .embeddings import EmbeddingGenerator

__all__ = [
    "DocumentLoader",
    "DocumentChunker",
    "EmbeddingGenerator",
]
