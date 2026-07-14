# System Architecture

```mermaid
flowchart TD

    User --> API

    API --> Orchestrator

    Orchestrator --> Planner
    Orchestrator --> Knowledge
    Orchestrator --> Safety
    Orchestrator --> Response

    Knowledge --> RAG

    RAG --> Documents
    RAG --> Embeddings
    RAG --> VectorIndex

    Memory --> Orchestrator

    Response --> AzureOpenAI
```