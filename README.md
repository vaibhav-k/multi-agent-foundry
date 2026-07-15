# Multi-Agent Foundry

> A modular Multi-Agent AI framework built with Retrieval-Augmented Generation (RAG), Azure OpenAI, FastAPI, conversation memory, evaluation pipelines, and production-ready orchestration.

---

# Table of Contents

1. Introduction
2. Features
3. Architecture
4. Technology Stack
5. Repository Structure
6. Documentation
7. Installation
8. Environment Configuration
9. Running the Application
10. Running Tests
11. Evaluation Framework
12. Development Workflow

---

# 1. Introduction

Multi-Agent Foundry is a production-oriented framework for building intelligent enterprise conversational assistants using multiple specialized AI agents.

Instead of relying on a single LLM to handle every responsibility, the system separates tasks into specialized components.

The framework separates reasoning, knowledge retrieval, validation, and response generation into independent components.

The architecture enables modular development, testing, evaluation, and extension of enterprise AI assistants. It follows separation of concerns, allowing each subsystem to be independently developed, tested, evaluated, and extended.

---

# 2. Features

## Multi-Agent Architecture

The application uses specialized AI agents instead of a single monolithic workflow. Each agent has a focused responsibility within the overall execution pipeline.

Included agents:

* Planner Agent
* Knowledge Agent
* Safety Agent
* Response Agent

Agent responsibilities:

| Agent | Responsibility |
|-------|---------------|
| Planner Agent | Analyzes user requests and determines execution workflow. |
| Knowledge Agent | Performs enterprise knowledge retrieval, RAG processing, answer generation, and citation creation. |
| Safety Agent | Validates generated responses against safety and grounding policies. |
| Response Agent | Produces the final user-facing response after validation. |

The agents communicate through shared workflow state managed by the orchestrator.

---

## Retrieval-Augmented Generation (RAG)

The RAG pipeline enables responses grounded in enterprise documentation.

Capabilities include:

* Document loading
* Text chunking
* Embedding generation
* Vector indexing
* Semantic retrieval
* Result re-ranking
* Grounded answer generation
* Citation generation
* Citation deduplication
* Retrieval evaluation

The Knowledge Agent orchestrates the RAG pipeline:

```text
              User Query

              |
              v

              Query Rewrite

              |
              v

              Document Retrieval

              |
              v

              Document Re-ranking

              |
              v

              Context Construction

              |
              v

              Grounded Answer Generation

              |
              v

              Citation Builder
```

---

## Conversation Memory

The framework supports contextual conversations through a dedicated memory layer.

Capabilities include:

* Conversation history
* Session state management
* Memory abstraction
* Context-aware responses

---

## FastAPI REST API

The application exposes functionality through REST APIs.

Supported capabilities include:

* Chat interactions
* Health checks
* Agent workflow execution

Available endpoints:

| Endpoint | Purpose |
|----------|---------|
| `GET /health` | Application health check |
| `POST /chat` | Execute the multi-agent assistant workflow |

---

## Prompt Management

Prompt templates are stored externally as text files.

Benefits:

* Independent prompt iteration
* Easier experimentation
* Version-controlled prompt changes
* Separation of code and AI instructions

---

## Evaluation Framework

The project includes automated evaluation pipelines for:

* Retrieval quality
* Response quality
* Safety validation
* Adversarial testing

---

## Testing

The project includes automated validation through unit and integration test suites.

# 3. High-Level Architecture

```text
                          User
                           │
                           ▼
                    FastAPI Application
                           │
                           ▼
                      API Routes
                           │
                           ▼
                    Orchestrator
                           │
        ┌──────────────────┼──────────────────┐
        │                  │                  │
        ▼                  ▼                  ▼
 Planner Agent      Safety Agent      Knowledge Agent
                                             │
                                             ▼
                                      RAG Pipeline
                                             │
                  ┌──────────────────────────┴──────────────────────────┐
                  ▼                                                     ▼
          Vector Retrieval                                      Document Sources
                  │
                  ▼
          Retrieved Context
                  │
                  ▼
           Generated Answer
                  │
                  ▼
           Safety Validation
                  │
                  ▼
           Response Agent
                  │
                  ▼
             Final Answer
```

---

# 4. Technology Stack

## Programming Language

* Python 3.11+

---

## Web Framework

* FastAPI

---

## AI Platform

* Azure OpenAI

---

## Retrieval

* Embeddings
* Vector search
* Semantic retrieval
* Re-ranking

---

## Testing

* pytest

---

## Configuration

* Environment variables
* python-dotenv

---

# 5. Repository Structure

```text
multi-agent-foundry/
│
├── src/
│   │
│   ├── agents/
│   │   ├── base.py
│   │   ├── planner.py
│   │   ├── knowledge.py
│   │   ├── safety.py
│   │   ├── response.py
│   │   └── __init__.py
│   │
│   ├── api/
│   │   ├── app.py
│   │   ├── dependencies.py
│   │   ├── routes.py
│   │   └── schemas.py
│   │
│   ├── config/
│   │   ├── client.py
│   │   ├── logger.py
│   │   ├── logging.py
│   │   ├── settings.py
│   │   └── __init__.py
│   │
│   ├── evaluation/
│   │   ├── dataset.py
│   │   ├── evaluator.py
│   │   ├── metrics.py
│   │   ├── models.py
│   │   ├── reports.py
│   │   └── samples/
│   │       ├── adversarial_questions.json
│   │       ├── rag_questions.json
│   │       └── security_questions.json
│   │
│   ├── memory/
│   │   ├── base.py
│   │   ├── conversation.py
│   │   └── store.py
│   │
│   ├── orchestrator/
│   │   ├── orchestrator.py
│   │   ├── router.py
│   │   ├── state.py
│   │   └── __init__.py
│   │
│   ├── prompts/
│   │   ├── system.txt
│   │   ├── planner.txt
│   │   ├── knowledge.txt
│   │   ├── safety.txt
│   │   ├── rag_answer.txt
│   │   ├── query_rewrite.txt
│   │   ├── citation.txt
│   │   └── __init__.py
│   │
│   ├── rag/
│   │   ├── chunker.py
│   │   ├── documents.py
│   │   ├── embeddings.py
│   │   ├── evaluation.py
│   │   ├── index.py
│   │   ├── ingestion.py
│   │   ├── loader.py
│   │   ├── models.py
│   │   ├── pipeline.py
│   │   ├── query.py
│   │   ├── reranker.py
│   │   ├── retriever.py
│   │   ├── search.py
│   │   ├── validators.py
│   │   ├── citations.py
│   │   └── sample_docs/
│   │       ├── access_management.md
│   │       ├── email_setup.md
│   │       ├── incident_reporting.md
│   │       ├── mfa_setup.md
│   │       ├── password_policy.md
│   │       ├── software_installation.md
│   │       └── vpn.md
│   │
│   ├── state/
│   │   └── models.py
│   │
│   ├── utils/
│   │   └── formatter.py
│   │
│   ├── bootstrap.py
│   ├── main.py
│   ├── models.py
│   └── __init__.py
│
├── tests/
│   │
│   ├── unit/
│   │   ├── test_chunker.py
│   │   ├── test_citations.py
│   │   ├── test_memory.py
│   │   ├── test_models.py
│   │   ├── test_orchestrator.py
│   │   ├── test_prompts.py
│   │   ├── test_query.py
│   │   ├── test_rag.py
│   │   ├── test_response_agent.py
│   │   ├── test_reranker.py
│   │   └── test_state.py
│   │
│   ├── integration/
│   │   ├── test_azure_connection.py
│   │   ├── test_content_safety.py
│   │   ├── test_rag_pipeline.py
│   │   ├── test_rag_quality.py
│   │   └── test_search.py
│   │
│   └── conftest.py
│
├── docs/
│   ├── architecture/
│   │   ├── system-architecture.md
│   │   ├── agent-flow.md
│   │   └── rag-pipeline.md
│   │
│   ├── agents.md
│   ├── api.md
│   ├── config.md
│   ├── evaluation.md
│   ├── memory.md
│   ├── orchestrator.md
│   ├── prompts.md
│   ├── rag.md
│   └── state-and-utils.md
│
├── scripts/
│   └── evaluate.py
│
├── .env
├── .env.example
├── .gitignore
├── pyproject.toml
├── pytest.ini
├── requirements.txt
├── README.md
└── LICENSE
```

---

# 6. Documentation

Detailed architecture and module documentation:

* [Project Overview](docs/Enterprise%20IT%20Knowledge%20Assistant.md)
* [Agents](docs/agents.md)
* [API](docs/api.md)
* [Configuration](docs/config.md)
* [Memory](docs/memory.md)
* [Orchestrator](docs/orchestrator.md)
* [Prompts](docs/prompts.md)
* [RAG](docs/rag.md)
* [Evaluation](docs/evaluation.md)
* [State and Utilities](docs/state-and-utils.md)

## Architecture Diagrams

Visual system documentation:

- [System Architecture](docs/architecture/system-architecture.md)
- [Agent Flow](docs/architecture/agent-flow.md)
- [RAG Pipeline](docs/architecture/rag-pipeline.md)

---

# 7. Installation

## Clone Repository

```bash
git clone https://github.com/vaibhav-k/multi-agent-foundry.git

cd multi-agent-foundry
```

---

## Create Virtual Environment

### Windows

```bash
python -m venv .venv

.venv\Scripts\activate
```

### Linux/macOS

```bash
python3 -m venv .venv

source .venv/bin/activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

# 8. Environment Configuration

Create a local `.env` file.

Example:

```env
AZURE_OPENAI_ENDPOINT=
AZURE_OPENAI_API_KEY=
AZURE_OPENAI_DEPLOYMENT=
AZURE_OPENAI_EMBEDDING_DEPLOYMENT=

LOG_LEVEL=INFO
```

Configuration values should remain local and must not be committed to version control.

---

# 9. Running the Application

Start the API server:

```bash
python -m src.main
```

or:

```bash
uvicorn src.api.app:app --reload
```

---

# 10. Running Tests

Run all tests:

```bash
pytest
```

Run unit tests:

```bash
pytest tests/unit
```

Run integration tests:

```bash
pytest tests/integration
```

---

# 11. Evaluation Framework

Run the evaluation pipeline:

```bash
python scripts/evaluate.py
```

The evaluation framework measures:

* Retrieval performance
* Response quality
* Safety behavior
* Adversarial robustness

Evaluation datasets are located at:

```text
src/evaluation/samples/
```

---

# 12. Development Workflow

## Code Organization

The project follows a modular architecture:

```text
API
 │
 ▼
Orchestrator
 │
 ├── Agents
 │
 ├── Memory
 │
 ├── RAG
 │
 └── Evaluation
```

---

## Recommended development process:

1. Add or modify functionality.
2. Add unit tests.
3. Run integration tests.
4. Run evaluation datasets.
5. Update documentation.

---

# License

Add project licensing information here.

---