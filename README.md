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

Core responsibilities are distributed across agents:

* Planning user requests
* Retrieving enterprise knowledge
* Performing Retrieval-Augmented Generation (RAG)
* Enforcing safety policies
* Generating final responses

The architecture follows separation of concerns, allowing each subsystem to be independently developed, tested, evaluated, and extended.

---

# 2. Features

## Multi-Agent Architecture

The application uses specialized AI agents instead of a single monolithic workflow.

Included agents:

* Planner Agent
* Knowledge Agent
* Safety Agent
* Response Agent

Each agent has a focused responsibility within the overall workflow.

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
* Citation generation
* Retrieval evaluation

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
* Knowledge retrieval
* Health checks
* Evaluation execution

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

The repository includes:

* Unit tests
* Integration tests
* RAG pipeline tests
* Safety tests

---

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
│   ├── agents/
│   ├── api/
│   ├── config/
│   ├── evaluation/
│   ├── memory/
│   ├── orchestrator/
│   ├── prompts/
│   ├── rag/
│   ├── state/
│   └── utils/
│
├── tests/
├── scripts/
├── docs/
├── README.md
├── requirements.txt
├── pytest.ini
└── .env
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

## Recommended Development Process

1. Add or modify functionality.
2. Add unit tests.
3. Run integration tests.
4. Run evaluation datasets.
5. Update documentation.

---

# License

Add project licensing information here.

---