# Memory Module

## Directory Structure

```text id="w8f9qv"
src/
└── memory/
    ├── base.py
    ├── conversation.py
    └── store.py
```

---

# Overview

The `memory` package provides the conversation memory layer for the Multi-Agent Foundry application.

Memory enables the system to maintain context across multiple interactions by storing and retrieving previous conversation data. This allows agents to produce responses that consider earlier messages, user intent, and ongoing workflows.

The memory layer is intentionally separated from agents and orchestration logic, allowing different storage implementations to be introduced without changing the rest of the application.

---

# Memory Architecture

```text id="0o6v6w"
                 User Request
                       │
                       ▼
                API Layer
                       │
                       ▼
              Orchestrator
                       │
                       ▼
              Memory Manager
                       │
        ┌──────────────┴──────────────┐
        ▼                             ▼
 Conversation Memory            Storage Backend
        │                             │
        ▼                             ▼
 Message History              Persisted Data
```

---

# Memory Responsibilities

The memory module handles:

* Conversation history management.
* Message storage.
* Context retrieval.
* Session tracking.
* Memory lifecycle management.
* Storage abstraction.

---

# Design Goals

## Separation of Storage and Logic

The application should not depend on a specific database or storage mechanism.

The memory interface defines what operations are required, while storage implementations define how data is persisted.

---

## Agent Independence

Agents should not directly manage conversation history.

Instead:

```text
Agent
  │
  ▼
Memory Interface
  │
  ▼
Storage Layer
```

This keeps agents focused on reasoning tasks.

---

## Extensibility

Future implementations can support:

* In-memory storage.
* Redis.
* PostgreSQL.
* Cosmos DB.
* Vector memory stores.

without changing agent logic.

---

# File: `src/memory/base.py`

## Purpose

Defines the abstract interface for memory implementations.

This file establishes the contract that all memory providers must follow.

---

## Responsibilities

* Define required memory operations.
* Provide common memory behavior.
* Ensure consistent interaction with storage implementations.

---

## Typical Components

A base memory class may define methods such as:

```python
save_message()
get_history()
clear_memory()
```

---

## Expected Operations

### Store Conversation Data

Accept new messages and associate them with a conversation session.

---

### Retrieve Context

Return previous conversation messages required for generating a response.

---

### Clear Memory

Remove stored conversation data when required.

---

## Inputs

Typical inputs include:

* Conversation identifier.
* User message.
* Assistant response.
* Metadata.

---

## Outputs

Returns:

* Conversation history.
* Stored message objects.
* Memory state.

---

## Used By

* `conversation.py`
* `store.py`
* Orchestrator components

---

# File: `src/memory/conversation.py`

## Purpose

Provides conversation-specific memory management.

This module represents a user's interaction history and provides utilities for managing messages within a conversation session.

---

## Responsibilities

* Create conversation objects.
* Track messages.
* Maintain ordering.
* Store conversation metadata.
* Provide context windows.

---

## Conversation Model

A conversation typically contains:

```text
Conversation
    │
    ├── Conversation ID
    │
    ├── Created Timestamp
    │
    ├── User Messages
    │
    ├── Assistant Messages
    │
    └── Metadata
```

---

## Message Lifecycle

```text id="6r1p5s"
User Input
    │
    ▼
Create Message
    │
    ▼
Store Message
    │
    ▼
Retrieve History
    │
    ▼
Generate Context
```

---

## Responsibilities During Generation

Before an agent generates a response:

1. Retrieve previous conversation history.
2. Combine history with the current request.
3. Send context to the relevant agent.
4. Store the generated response.

---

## Used By

* Response Agent
* Orchestrator
* API layer

---

# File: `src/memory/store.py`

## Purpose

Implements the storage layer for conversation memory.

This module handles the actual persistence and retrieval of conversation data.

---

## Responsibilities

* Save conversations.
* Retrieve conversations.
* Update conversation state.
* Remove expired conversations.
* Manage storage lifecycle.

---

## Storage Options

Depending on implementation, this layer can support:

### In-Memory Storage

Useful for:

* Development
* Testing
* Local execution

---

### Database Storage

Suitable for:

* Production environments
* Persistent conversations
* Multi-user systems

---

### Distributed Storage

Examples:

* Redis
* Cloud databases
* Managed key-value stores

---

## Inputs

Examples:

* Conversation ID
* Message object
* Conversation state

---

## Outputs

Examples:

* Conversation history
* Stored message collection
* Storage confirmation

---

## Workflow

```text id="9c3g7v"
Application
     │
     ▼
Memory Store
     │
     ▼
Storage Backend
     │
     ▼
Persisted Conversation
```

---

# Memory Data Flow

```text id="ihv7yb"
                 New Request
                      │
                      ▼
             Retrieve Conversation
                      │
                      ▼
              Add User Message
                      │
                      ▼
              Execute AI Pipeline
                      │
                      ▼
            Store Assistant Response
                      │
                      ▼
              Updated Conversation
```

---

# Integration With Agents

Memory does not directly execute AI operations.

Instead, it provides context to agents.

Example:

```text
User:

"How do I configure VPN?"

Previous Context:

"User already configured MFA."

↓

Knowledge Agent receives:

Current Query + Conversation Context

↓

Response Agent generates:

Context-aware Answer
```

---

# Integration With Orchestrator

The orchestrator typically manages when memory is accessed.

Example workflow:

```text
Request Received

↓

Load Conversation History

↓

Create Agent State

↓

Execute Agents

↓

Save Updated Conversation

```

---

# Memory Design Principles

## Abstraction

The rest of the application interacts with memory through interfaces rather than storage details.

---

## Reliability

Memory operations should handle:

* Missing sessions
* Expired conversations
* Storage failures

---

## Privacy

Conversation data should be managed carefully.

Production implementations should consider:

* Data retention policies.
* Encryption.
* Access control.
* User isolation.

---

# Module Relationships

| Module              | Relationship                                         |
| ------------------- | ---------------------------------------------------- |
| `src/orchestrator/` | Coordinates when memory is read and updated.         |
| `src/state/`        | Stores runtime state exchanged between components.   |
| `src/agents/`       | Consumes conversation context for reasoning.         |
| `src/api/`          | Receives conversation identifiers and user requests. |
| `src/config/`       | Provides storage configuration.                      |
