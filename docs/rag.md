# Retrieval-Augmented Generation (RAG) Module

## Directory Structure

```text id="8r4vpd"
src/
└── rag/
    ├── __init__.py
    ├── chunker.py
    ├── citations.py
    ├── documents.py
    ├── embeddings.py
    ├── evaluation.py
    ├── index.py
    ├── ingestion.py
    ├── loader.py
    ├── models.py
    ├── pipeline.py
    ├── query.py
    ├── reranker.py
    ├── retriever.py
    ├── search.py
    ├── validators.py
    │
    └── sample_docs/
        ├── access_management.md
        ├── email_setup.md
        ├── incident_reporting.md
        ├── mfa_setup.md
        ├── password_policy.md
        ├── software_installation.md
        └── vpn.md
```

---

# Overview

The `rag` package implements the Retrieval-Augmented Generation pipeline used by the Knowledge Agent.

RAG improves language model responses by combining the reasoning capability of an LLM with external knowledge retrieval. Instead of relying only on model training data, the system retrieves relevant documents and provides them as context during generation.

The RAG pipeline enables the application to answer questions using organization-specific documentation.

---

# RAG Architecture

```text id="9n8s6v"
                  Documents
                      │
                      ▼
                Document Loader
                      │
                      ▼
                  Chunker
                      │
                      ▼
                Embeddings
                      │
                      ▼
                 Vector Index
                      │
                      ▼
                 Retriever
                      │
                      ▼
                 Re-ranker
                      │
                      ▼
              Retrieved Context
                      │
                      ▼
              Response Generation
                      │
                      ▼
                  Final Answer
```

---

# RAG Pipeline Stages

## 1. Document Loading

Documents are loaded from supported sources and converted into internal document objects.

---

## 2. Document Chunking

Large documents are divided into smaller sections suitable for embedding and retrieval.

---

## 3. Embedding Generation

Text chunks are converted into numerical vectors representing semantic meaning.

---

## 4. Index Creation

Embeddings are stored in a searchable index.

---

## 5. Retrieval

User queries are converted into embeddings and matched against indexed content.

---

## 6. Re-ranking

Retrieved results are scored and reordered based on relevance.

---

## 7. Context Construction

The most relevant information is assembled into context for the language model.

---

## 8. Answer Generation

The Response Agent generates an answer grounded in retrieved information.

---

# File: `src/rag/__init__.py`

## Purpose

Initializes the RAG package.

---

## Responsibilities

* Package initialization.
* Optional exports.
* Import organization.

---

## Dependencies

None.

---

# File: `src/rag/models.py`

## Purpose

Defines data models used throughout the RAG pipeline.

---

## Responsibilities

Represents:

* Documents.
* Chunks.
* Retrieval results.
* Metadata.
* Search results.

---

## Typical Models

### Document

Represents a complete source document.

Example:

```text id="w5y83m"
Document
 ├── id
 ├── title
 ├── content
 └── metadata
```

---

### Chunk

Represents a searchable document segment.

Example:

```text id="8x9z5w"
Chunk
 ├── text
 ├── document_id
 ├── position
 └── metadata
```

---

### Retrieval Result

Contains:

* Matching text.
* Similarity score.
* Source information.

---

## Used By

Almost every RAG component.

---

# File: `src/rag/documents.py`

## Purpose

Provides document-related utilities and abstractions.

---

## Responsibilities

* Create document objects.
* Manage document metadata.
* Normalize document structure.
* Validate document content.

---

## Used By

* Loader.
* Chunker.
* Ingestion pipeline.

---

# File: `src/rag/loader.py`

## Purpose

Loads documents into the RAG pipeline.

---

## Responsibilities

* Read files.
* Extract text.
* Create document objects.
* Attach metadata.

---

## Supported Sources

Depending on implementation:

* Markdown files.
* Text files.
* PDFs.
* Knowledge repositories.

---

## Workflow

```text id="3frfkn"
Source Document

↓

Loader

↓

Document Object

↓

Chunking
```

---

# File: `src/rag/chunker.py`

## Purpose

Splits documents into smaller searchable chunks.

---

## Why Chunking Is Required

Language models and vector search systems work better with focused pieces of information rather than large documents.

---

## Responsibilities

* Split text.
* Preserve context.
* Apply overlap.
* Generate chunk metadata.

---

## Input

Document object.

---

## Output

List of chunks.

---

## Example

```text id="4x3qfh"
Large Document

        │

        ▼

Chunk 1
Chunk 2
Chunk 3
```

---

# File: `src/rag/embeddings.py`

## Purpose

Generates vector representations of text.

---

## Responsibilities

* Convert text into embeddings.
* Interface with embedding models.
* Handle embedding requests.

---

## Input

Text chunks.

---

## Output

Numerical vectors.

---

## Workflow

```text id="6z1h49"
Text

↓

Embedding Model

↓

Vector Representation
```

---

# File: `src/rag/index.py`

## Purpose

Manages the searchable vector index.

---

## Responsibilities

* Store embeddings.
* Add documents.
* Remove documents.
* Execute vector operations.

---

## Index Operations

Typical operations:

* Insert vectors.
* Search vectors.
* Update records.
* Delete records.

---

# File: `src/rag/ingestion.py`

## Purpose

Coordinates document ingestion into the RAG system.

---

## Responsibilities

Combines:

* Loading.
* Cleaning.
* Chunking.
* Embedding.
* Indexing.

---

## Workflow

```text id="q98f6d"
Document Source

↓

Loader

↓

Chunker

↓

Embeddings

↓

Index
```

---

# File: `src/rag/retriever.py`

## Purpose

Retrieves relevant documents based on user queries.

---

## Responsibilities

* Convert query into searchable form.
* Execute similarity search.
* Return relevant chunks.

---

## Inputs

* Search query.
* Retrieval configuration.

---

## Outputs

Relevant document chunks.

---

# File: `src/rag/search.py`

## Purpose

Provides search functionality used by retrieval components.

---

## Responsibilities

* Execute search operations.
* Manage search parameters.
* Normalize search results.

---

## Used By

* Retriever.
* Knowledge Agent.

---

# File: `src/rag/query.py`

## Purpose

Handles query preparation before retrieval.

---

## Responsibilities

* Query normalization.
* Query rewriting.
* Search optimization.

---

## Used By

* Planner Agent.
* Knowledge Agent.

---

# File: `src/rag/reranker.py`

## Purpose

Improves retrieval quality by reordering search results.

---

## Why Re-ranking Is Needed

Initial vector search may return semantically related but less useful results.

The reranker identifies the most relevant information.

---

## Workflow

```text id="zqf2k4"
Retrieved Results

↓

Reranker

↓

Ranked Results
```

---

# File: `src/rag/citations.py`

## Purpose

Generates source references for retrieved information.

---

## Responsibilities

* Track document sources.
* Attach citations.
* Format references.

---

## Benefits

Provides:

* Transparency.
* Traceability.
* User confidence.

---

# File: `src/rag/validators.py`

## Purpose

Validates RAG inputs and outputs.

---

## Responsibilities

* Validate documents.
* Validate chunks.
* Check retrieval quality.
* Detect invalid states.

---

# File: `src/rag/evaluation.py`

## Purpose

Provides evaluation utilities specific to the RAG pipeline.

---

## Responsibilities

Measures:

* Retrieval relevance.
* Context quality.
* Answer grounding.

---

# Sample Documents

## Directory

```text id="4k4s7d"
src/rag/sample_docs/
```

---

## Purpose

Contains example knowledge base documents used for testing and demonstration.

---

## Files

| File                       | Purpose                            |
| -------------------------- | ---------------------------------- |
| `access_management.md`     | User access procedures.            |
| `email_setup.md`           | Email configuration instructions.  |
| `incident_reporting.md`    | Incident handling process.         |
| `mfa_setup.md`             | Multi-factor authentication setup. |
| `password_policy.md`       | Password requirements.             |
| `software_installation.md` | Software installation process.     |
| `vpn.md`                   | VPN configuration guidance.        |

---

# RAG Integration With Agents

```text id="xmz4y1"
User Question

↓

Planner Agent

↓

Knowledge Agent

↓

RAG Pipeline

↓

Retrieved Context

↓

Response Agent

↓

Final Answer
```

---

# RAG Design Principles

## Grounded Responses

Answers should be based on retrieved information.

---

## Modular Components

Each stage of the pipeline can be replaced independently.

---

## Evaluation Driven

Retrieval quality should be measured continuously.

---

## Source Transparency

Responses should preserve document references whenever possible.

---

# Module Relationships

| Module                    | Relationship                                   |
| ------------------------- | ---------------------------------------------- |
| `src/agents/knowledge.py` | Uses RAG for information retrieval.            |
| `src/prompts/`            | Provides prompts for retrieval and generation. |
| `src/orchestrator/`       | Coordinates RAG execution.                     |
| `src/evaluation/`         | Measures RAG quality.                          |
| `src/config/`             | Provides model and service configuration.      |
