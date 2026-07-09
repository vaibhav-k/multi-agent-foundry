"""
RAG domain models.

Defines document and chunk structures
used throughout the retrieval pipeline.
"""

from typing import Dict, Optional

from pydantic import BaseModel, Field


class DocumentMetadata(BaseModel):
    """
    Metadata associated with an enterprise document.
    """

    source: str

    title: Optional[str] = None

    department: Optional[str] = "IT"

    classification: Optional[str] = "internal"


class Document(BaseModel):
    """
    Enterprise source document.
    """

    document_id: str

    content: str

    metadata: DocumentMetadata


class DocumentChunk(BaseModel):
    """
    Searchable document chunk.
    """

    chunk_id: str

    document_id: str

    content: str

    metadata: Dict[str, str] = Field(default_factory=dict)

    section: Optional[str] = None

    chunk_number: int
