# Agents Module

## Directory

```text
src/
└── agents/
    ├── __init__.py
    ├── base.py
    ├── planner.py
    ├── knowledge.py
    ├── response.py
    └── safety.py
```

---

# Overview

The `agents` package contains the core intelligence layer of the Multi-Agent Foundry application. Each agent has a single responsibility and is orchestrated as part of the request-processing pipeline.

Unlike a monolithic AI application where a single model handles every task, this project decomposes the workflow into specialized agents. This separation improves maintainability, extensibility, and testing while allowing each agent to focus on a specific capability.

Typical responsibilities include:

* Planning the execution strategy
* Retrieving enterprise knowledge
* Applying safety policies
* Generating the final response

The orchestrator coordinates these agents, passing a shared state object between them until the final response is produced.

---

# Agent Execution Flow

```text
                    User Request
                          │
                          ▼
                  Planner Agent
                          │
                          ▼
                 Knowledge Agent
                          │
                          ▼
                   Safety Agent
                          │
                          ▼
                  Response Agent
                          │
                          ▼
                    Final Response
```

---

# Module Dependencies

```text
                    Orchestrator
                          │
                          ▼
                     BaseAgent
                          │
      ┌──────────────┬────┴─────┬──────────────┐
      ▼              ▼          ▼              ▼
 PlannerAgent  KnowledgeAgent SafetyAgent ResponseAgent
                     │
                     ▼
                RAG Pipeline
```

---

# File: `src/agents/__init__.py`

## Purpose

Marks the `agents` directory as a Python package and optionally exposes commonly used agent classes for simplified imports.

---

## Responsibilities

* Package initialization.
* Export commonly used classes.
* Simplify import statements across the application.

---

## Typical Usage

Instead of:

```python
from src.agents.planner import PlannerAgent
```

developers may write:

```python
from src.agents import PlannerAgent
```

when the package exports are defined.

---

## Dependencies

None.

---

# File: `src/agents/base.py`

## Purpose

Defines the abstract base implementation shared by every specialized agent.

Every agent should inherit from this class to ensure a consistent interface and shared functionality.

---

## Responsibilities

* Define the common execution interface.
* Initialize shared resources.
* Configure Azure OpenAI clients.
* Manage logging.
* Handle exceptions consistently.
* Provide helper utilities for derived classes.

---

## Expected Components

Typical implementations include:

* `BaseAgent`
* Abstract `run()` or `execute()` method
* Shared configuration
* Logging helpers
* Common prompt execution methods

---

## Inputs

Depending on the implementation, the base agent typically receives:

* Conversation state
* User request
* Configuration
* Runtime context

---

## Outputs

Returns an updated state object or structured response to the orchestrator.

---

## Used By

* `planner.py`
* `knowledge.py`
* `response.py`
* `safety.py`

---

## Workflow

```text
Create Agent
      │
      ▼
Initialize Dependencies
      │
      ▼
Receive State
      │
      ▼
Execute Logic
      │
      ▼
Return Updated State
```

---

## Design Considerations

The base class should avoid implementing business-specific logic. Its role is to provide reusable infrastructure that all agents can inherit.

---

# File: `src/agents/planner.py`

## Purpose

The Planner Agent analyzes incoming user requests and determines how they should be processed by the remainder of the system.

It acts as the decision-making component of the multi-agent architecture.

---

## Responsibilities

* Interpret user intent.
* Rewrite ambiguous queries.
* Determine whether retrieval is required.
* Identify missing information.
* Produce an execution plan.
* Classify request type.

---

## Inputs

* User prompt
* Conversation history
* Current conversation state

---

## Outputs

Planning metadata such as:

* Task type
* Retrieval requirement
* Rewritten query
* Execution instructions

---

## Dependencies

* `src/prompts/planner.txt`
* `src/state/models.py`
* `src/models.py`

---

## Used By

* `src/orchestrator/router.py`
* `src/orchestrator/orchestrator.py`

---

## Typical Workflow

```text
User Query
      │
      ▼
Intent Detection
      │
      ▼
Task Classification
      │
      ▼
Query Rewriting
      │
      ▼
Execution Plan
```

---

## Example Responsibilities

Examples of planning decisions include:

* Should the RAG pipeline be invoked?
* Can the question be answered directly?
* Does the request require clarification?
* Should safety checks receive higher priority?

---

# File: `src/agents/knowledge.py`

## Purpose

The Knowledge Agent is responsible for interacting with the Retrieval-Augmented Generation (RAG) subsystem.

It retrieves the most relevant information from indexed documents and prepares contextual data for the language model.

---

## Responsibilities

* Execute semantic search.
* Retrieve document chunks.
* Apply relevance filtering.
* Re-rank search results.
* Assemble contextual information.
* Produce citation metadata.

---

## Inputs

* Optimized query
* Planner instructions
* Retrieval configuration

---

## Outputs

Typically returns:

* Retrieved document chunks
* Confidence scores
* Citation information
* Context package

---

## Dependencies

* `src/rag/pipeline.py`
* `src/rag/retriever.py`
* `src/rag/reranker.py`
* `src/rag/search.py`
* `src/rag/citations.py`

---

## Workflow

```text
Optimized Query
       │
       ▼
Embedding Search
       │
       ▼
Retrieved Documents
       │
       ▼
Re-ranking
       │
       ▼
Context Assembly
```

---

## Integration

The Knowledge Agent is the primary consumer of the RAG subsystem and serves as the bridge between retrieval and response generation.

---

# File: `src/agents/safety.py`

## Purpose

The Safety Agent ensures that both incoming requests and generated responses comply with defined safety policies.

This component helps prevent unsafe, inappropriate, or restricted content from being returned to users.

---

## Responsibilities

* Validate user prompts.
* Apply moderation policies.
* Detect policy violations.
* Filter unsafe outputs.
* Produce moderation decisions.

---

## Inputs

* User request
* Retrieved context
* Generated response

---

## Outputs

* Approval or rejection
* Safety annotations
* Policy decision
* Updated state

---

## Dependencies

* `src/prompts/safety.txt`
* Azure Content Safety (if configured)

---

## Workflow

```text
Request
   │
   ▼
Policy Evaluation
   │
   ▼
Moderation Decision
   │
   ▼
Approved Response
```

---

## Typical Checks

* Prompt injection attempts
* Harmful content
* Sensitive information
* Restricted instructions
* Organizational policy violations

---

# File: `src/agents/response.py`

## Purpose

The Response Agent is responsible for generating the final answer that will be returned to the client.

It combines the user request, retrieved context, prompt templates, and conversation history into a complete prompt for the language model.

---

## Responsibilities

* Assemble the final prompt.
* Incorporate retrieved knowledge.
* Generate citations.
* Produce a formatted response.
* Attach metadata.

---

## Inputs

* User request
* Conversation history
* Retrieved documents
* Prompt templates
* Planner output

---

## Outputs

The final response typically includes:

* Answer text
* Citations
* Metadata
* Confidence information (if applicable)

---

## Dependencies

* `src/prompts/rag_answer.txt`
* `src/rag/citations.py`
* Azure OpenAI client

---

## Workflow

```text
Retrieved Context
        │
        ▼
Prompt Construction
        │
        ▼
Language Model
        │
        ▼
Citation Formatting
        │
        ▼
Final Response
```

---

# Agent Collaboration

The following diagram illustrates how agents cooperate during request processing.

```text
                  User Request
                        │
                        ▼
                  Planner Agent
                        │
        Determines execution strategy
                        │
                        ▼
                Knowledge Agent
                        │
          Retrieves supporting context
                        │
                        ▼
                 Safety Agent
                        │
         Validates request and output
                        │
                        ▼
                Response Agent
                        │
         Generates final user response
                        │
                        ▼
                     Client
```

---

# Design Principles

The `agents` package follows several software engineering principles:

## Single Responsibility Principle

Each agent performs one clearly defined task.

## Loose Coupling

Agents communicate through shared state managed by the orchestrator rather than directly invoking one another.

## Extensibility

New agents can be introduced without modifying existing implementations, provided they adhere to the common interface.

## Reusability

Common functionality is centralized in `base.py` to reduce duplication.

## Testability

Each agent can be unit tested independently by mocking external dependencies such as the language model or retrieval pipeline.

---

# Related Modules

| Module              | Purpose                                                      |
| ------------------- | ------------------------------------------------------------ |
| `src/orchestrator/` | Coordinates execution of all agents.                         |
| `src/rag/`          | Provides retrieval capabilities used by the Knowledge Agent. |
| `src/prompts/`      | Contains prompt templates used by multiple agents.           |
| `src/state/`        | Defines the shared state exchanged between agents.           |
| `src/config/`       | Supplies configuration and client initialization.            |