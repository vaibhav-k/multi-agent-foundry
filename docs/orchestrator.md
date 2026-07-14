# Orchestrator Module

## Directory Structure

```text id="q4o5w7"
src/
└── orchestrator/
    ├── __init__.py
    ├── orchestrator.py
    ├── router.py
    └── state.py
```

---

# Overview

The `orchestrator` package is the central coordination layer of the Multi-Agent Foundry application.

It controls the execution flow between different agents, manages shared state, determines which components should participate in processing, and ensures that information flows correctly through the AI pipeline.

The orchestrator acts as the workflow engine of the system.

Instead of agents directly calling each other, the orchestrator coordinates execution:

```text
User Request
      │
      ▼
Orchestrator
      │
      ├── Planner Agent
      │
      ├── Knowledge Agent
      │
      ├── Safety Agent
      │
      └── Response Agent
      │
      ▼
Final Response
```

---

# Core Responsibilities

The orchestrator manages:

* Agent execution order.
* Routing decisions.
* Shared state propagation.
* Error handling.
* Pipeline lifecycle.
* Agent communication.

---

# Architecture

```text
                         Request
                            │
                            ▼
                    Orchestrator
                            │
              ┌─────────────┴─────────────┐
              ▼                           ▼
          Router                    State Manager
              │                           │
              ▼                           │
       Agent Selection                    │
              │                           │
      ┌───────┼────────┬────────┐         │
      ▼       ▼        ▼        ▼         │
 Planner Knowledge Safety Response       │
      │       │        │        │         │
      └───────┴────────┴────────┘         │
                    │                     │
                    ▼                     │
             Updated Application State ◄──┘
```

---

# File: `src/orchestrator/__init__.py`

## Purpose

Initializes the orchestrator package.

It may expose frequently used orchestration classes to simplify imports.

---

## Responsibilities

* Package initialization.
* Optional exports.
* Import organization.

---

## Dependencies

None.

---

# File: `src/orchestrator/orchestrator.py`

## Purpose

Implements the primary workflow controller responsible for coordinating all agents.

This is the main execution engine of the multi-agent system.

---

# Responsibilities

## Agent Coordination

The orchestrator determines:

* Which agents execute.
* In what order they execute.
* What information each agent receives.

---

## State Management

Maintains the shared state object as it moves through the pipeline.

Example:

```text
Initial State

↓

Planner Updates State

↓

Knowledge Adds Context

↓

Safety Adds Validation

↓

Response Adds Final Answer
```

---

## Error Handling

Manages failures from:

* Agent execution.
* External services.
* Retrieval systems.
* Model calls.

---

## Pipeline Execution

Controls the full lifecycle:

```text
Receive Request

↓

Create State

↓

Execute Agents

↓

Collect Results

↓

Return Response
```

---

# Inputs

Typical inputs include:

* User request.
* Conversation history.
* Runtime configuration.
* User/session metadata.

---

# Outputs

Returns:

* Final generated response.
* Updated conversation state.
* Metadata.
* Execution information.

---

# Dependencies

Common dependencies:

* `agents/*`
* `router.py`
* `state.py`
* `memory/*`
* `config/*`

---

# Execution Flow

```text
                 User Request
                       │
                       ▼
              Create Initial State
                       │
                       ▼
                Route Request
                       │
                       ▼
              Execute Planner
                       │
                       ▼
            Execute Knowledge Agent
                       │
                       ▼
             Execute Safety Agent
                       │
                       ▼
             Execute Response Agent
                       │
                       ▼
               Return Final Output
```

---

# File: `src/orchestrator/router.py`

## Purpose

Determines the execution path for incoming requests.

The router decides which agents or workflows should be activated based on the request characteristics.

---

# Responsibilities

* Classify requests.
* Select required agents.
* Determine workflow path.
* Handle simple versus complex requests.

---

# Example Decisions

A router may determine:

### General Question

```text
User:

"What is MFA?"

↓

Planner

↓

Knowledge Agent

↓

Response Agent
```

---

### Restricted Request

```text
User:

"Provide restricted credentials"

↓

Safety Agent

↓

Reject Request
```

---

### Multi-step Task

```text
User:

"Help configure VPN access"

↓

Planner

↓

Knowledge Agent

↓

Response Agent
```

---

# Inputs

* User query.
* Conversation state.
* Classification metadata.

---

# Outputs

A routing decision containing:

* Selected agents.
* Execution order.
* Workflow type.

---

# Dependencies

* Agent definitions.
* State models.
* Configuration.

---

# File: `src/orchestrator/state.py`

## Purpose

Defines orchestration-specific runtime state.

This state object carries information between agents during execution.

---

# Responsibilities

Maintains:

* User input.
* Agent outputs.
* Retrieved context.
* Execution metadata.
* Errors.
* Final response.

---

# Example State Lifecycle

```text
Initial State

{
 query: "How do I setup VPN?"
}

        │

Planner

{
 query: "...",
 intent: "configuration",
 requires_rag: true
}

        │

Knowledge

{
 documents: [...],
 citations: [...]
}

        │

Response

{
 answer: "...",
 citations: [...]
}
```

---

# State Components

A typical state may contain:

| Field             | Description               |
| ----------------- | ------------------------- |
| `query`           | Original user request     |
| `conversation_id` | Active session identifier |
| `messages`        | Conversation history      |
| `plan`            | Planner output            |
| `context`         | Retrieved documents       |
| `safety_result`   | Safety evaluation         |
| `response`        | Generated answer          |
| `metadata`        | Runtime information       |

---

# State Flow

```text
              Request
                 │
                 ▼
          Initial State
                 │
                 ▼
        Planner Modification
                 │
                 ▼
        Knowledge Modification
                 │
                 ▼
         Safety Modification
                 │
                 ▼
        Response Modification
                 │
                 ▼
          Completed State
```

---

# Agent Communication Model

Agents communicate indirectly through state.

Example:

```text
Planner Agent

Input:
User Question

Output:
Updated State


Knowledge Agent

Input:
State with Plan

Output:
State with Documents


Response Agent

Input:
State with Context

Output:
State with Answer
```

This approach avoids tight coupling between agents.

---

# Error Handling Strategy

The orchestrator should provide centralized handling for:

* Agent failures.
* Timeout errors.
* Model failures.
* Retrieval failures.
* Invalid states.

Possible strategies:

* Retry failed operations.
* Skip optional agents.
* Return graceful error responses.
* Log execution failures.

---

# Design Principles

## Centralized Control

The orchestrator owns workflow decisions rather than individual agents.

---

## Loose Coupling

Agents communicate through state objects rather than direct references.

---

## Observability

Execution metadata can be collected for:

* Debugging.
* Performance monitoring.
* Evaluation.

---

## Extensibility

New agents can be added by:

1. Implementing the agent interface.
2. Registering the agent.
3. Updating routing logic.

---

# Module Relationships

| Module            | Relationship                                                     |
| ----------------- | ---------------------------------------------------------------- |
| `src/agents/`     | Provides the specialized workers controlled by the orchestrator. |
| `src/state/`      | Defines shared data structures used during execution.            |
| `src/memory/`     | Provides conversation history.                                   |
| `src/rag/`        | Supplies knowledge retrieval capabilities.                       |
| `src/api/`        | Sends user requests into the orchestration workflow.             |
| `src/evaluation/` | Measures orchestration and response quality.                     |
