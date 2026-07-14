# State and Utilities Module

## Directory Structure

```text id="x4f1zq"
src/
│
├── state/
│   └── models.py
│
└── utils/
    ├── __init__.py
    └── formatter.py
```

---

# Overview

The `state` and `utils` packages provide supporting infrastructure used throughout the Multi-Agent Foundry application.

The `state` package defines the shared data structures exchanged between components during execution, while the `utils` package contains reusable helper functions that simplify common operations.

These modules do not contain major business logic. Instead, they provide common building blocks that improve consistency across the application.

---

# Architecture

```text id="5zv2ki"
                 Application Request

                         │

                         ▼

                   Shared State

                         │

        ┌────────────────┼────────────────┐

        ▼                ▼                ▼

     Agents        Orchestrator        RAG

                         │

                         ▼

                    Utilities
```

---

# State Module

## Directory

```text id="m2wq2h"
src/
└── state/
    └── models.py
```

---

# Purpose

The `state` package defines the runtime state objects used throughout the multi-agent workflow.

Agents do not directly communicate with one another. Instead, they receive and update a shared state object managed by the orchestrator.

This creates a predictable communication pattern:

```text id="8f9j2e"
Agent A

    │

    ▼

Shared State

    │

    ▼

Agent B
```

---

# File: `src/state/models.py`

## Purpose

Defines the application's execution state models.

These models represent information flowing through the AI pipeline.

---

# Responsibilities

The state model stores:

* User input.
* Conversation information.
* Agent outputs.
* Retrieved documents.
* Safety decisions.
* Generated responses.
* Execution metadata.

---

# State Lifecycle

```text id="r2w5xk"
Initial Request

      │

      ▼

Initial State Created

      │

      ▼

Planner Updates State

      │

      ▼

Knowledge Agent Adds Context

      │

      ▼

Safety Agent Validates

      │

      ▼

Response Agent Generates Output

      │

      ▼

Completed State
```

---

# Typical State Structure

A state object may contain:

```text id="c3y8n4"
ApplicationState

├── request
│
├── conversation_id
│
├── messages
│
├── plan
│
├── retrieved_context
│
├── citations
│
├── safety_result
│
├── response
│
└── metadata
```

---

# Core Responsibilities

## Request Tracking

Stores the original user request throughout processing.

---

## Agent Communication

Provides a shared communication mechanism between agents.

---

## Context Preservation

Maintains information gathered during execution.

---

## Debugging Support

Allows developers to inspect intermediate execution states.

---

# Used By

* `src/orchestrator/orchestrator.py`
* `src/orchestrator/router.py`
* `src/agents/*`
* `src/memory/*`
* `src/api/*`

---

# Design Principles

## Immutable or Controlled Updates

State changes should be predictable and traceable.

---

## Strong Typing

Models should define clear data structures to reduce runtime errors.

---

## Minimal Coupling

State should contain data, not business logic.

---

# Utilities Module

## Directory

```text id="7x8m2q"
src/
└── utils/
    ├── __init__.py
    └── formatter.py
```

---

# Purpose

The utilities package contains reusable helper functions shared across multiple parts of the application.

Utilities should remain lightweight and generic.

---

# File: `src/utils/__init__.py`

## Purpose

Initializes the utilities package.

---

## Responsibilities

* Package initialization.
* Optional helper exports.

---

## Dependencies

None.

---

# File: `src/utils/formatter.py`

## Purpose

Provides formatting utilities used throughout the application.

---

# Responsibilities

Typical responsibilities include:

* Formatting responses.
* Cleaning text.
* Formatting citations.
* Normalizing output.
* Preparing display content.

---

# Possible Formatting Operations

## Text Formatting

Example:

```text id="x0d8za"
Raw Output

↓

Cleaned Output
```

---

## Citation Formatting

Transforms citation metadata into user-readable references.

Example:

```text id="2g4l6c"
Source:
vpn.md

↓

Reference:
According to VPN Setup Guide...
```

---

## Response Formatting

Ensures generated responses follow a consistent structure.

Example:

```text id="7b8m4s"
Answer

+

Sources

+

Metadata
```

---

# Used By

Potential consumers:

* `src/api/`
* `src/agents/response.py`
* `src/rag/citations.py`
* Evaluation reporting modules

---

# Utility Design Guidelines

## Keep Functions Stateless

Utilities should generally receive input and return output without maintaining internal state.

---

## Avoid Business Logic

Complex decisions belong in:

* Agents.
* Orchestrator.
* Services.

Utilities should only perform transformations.

---

## Reuse Instead of Duplicate

Common formatting operations should exist in one location instead of being duplicated across modules.

---

# Relationship Between State and Utilities

```text id="y6p4qz"
                 Agent Execution

                       │

                       ▼

                 Update State

                       │

                       ▼

             Format Using Utilities

                       │

                       ▼

               Return Response
```

---

# Integration With Application

```text id="9c4xqk"
                    API

                     │

                     ▼

              Orchestrator

                     │

        ┌────────────┴────────────┐

        ▼                         ▼

     State                    Utilities

        │                         │

        ▼                         ▼

     Agents                 Formatting

        │

        ▼

      RAG
```

---

# Best Practices

## Keep State Models Stable

Changes to state objects affect every component that consumes them.

---

## Document New Fields

Every state attribute should have a clear purpose.

---

## Test Utility Functions

Small helper functions should have unit tests because they are reused widely.

---

## Avoid Utility Overgrowth

If a utility starts containing business decisions, it should be moved into an appropriate service or module.
