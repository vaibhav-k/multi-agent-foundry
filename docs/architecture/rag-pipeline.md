# RAG Pipeline

```mermaid
flowchart LR

    Documents --> Loader

    Loader --> Chunker

    Chunker --> Embeddings

    Embeddings --> VectorIndex

    UserQuery --> Retriever

    VectorIndex --> Retriever

    Retriever --> Reranker

    Reranker --> Context

    Context --> LLM

    LLM --> Answer
```