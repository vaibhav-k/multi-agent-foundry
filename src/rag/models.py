"""
RAG data models.

Shared models used across:

- Document ingestion
- Embedding generation
- Azure AI Search
- Retrieval
- Reranking
- Citation generation
"""

from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class DocumentMetadata(BaseModel):
    """
    Metadata associated with enterprise documents.

    Used during ingestion and indexing.
    """

    source: Optional[str] = None

    title: Optional[str] = None

    section: Optional[str] = None

    document_type: Optional[str] = None

    author: Optional[str] = None

    created_at: Optional[str] = None

    extra: Dict[str, Any] = Field(default_factory=dict)


class RAGDocument(BaseModel):
    """
    Enterprise document representation.

    Common contract between:

    - Ingestion
    - Embeddings
    - Search
    - Retrieval
    - Reranking
    - Citations
    """

    document_id: str

    source: Optional[str] = None

    title: Optional[str] = None

    content: str

    embedding: Optional[List[float]] = None

    score: Optional[float] = None

    metadata: DocumentMetadata | Dict[str, Any] = Field(default_factory=dict)


class SearchResult(BaseModel):
    """
    Azure AI Search response wrapper.
    """

    query: str

    documents: List[RAGDocument] = Field(default_factory=list)


class DocumentChunk(BaseModel):
    """
    Intermediate chunk before embedding.
    """

    chunk_id: str

    source: Optional[str] = None

    title: Optional[str] = None

    content: str

    metadata: DocumentMetadata | Dict[str, Any] = Field(default_factory=dict)


class Citation(BaseModel):
    """
    Citation generated from retrieved documents.
    """

    document_id: Optional[str] = None

    source: Optional[str] = None

    title: Optional[str] = None

    score: Optional[float] = None

    section: Optional[str] = None
