# Prompt Management Module

## Directory Structure

```text id="4q6q8m"
src/
└── prompts/
    ├── __init__.py
    ├── citation.txt
    ├── knowledge.txt
    ├── planner.txt
    ├── query_rewrite.txt
    ├── rag_answer.txt
    └── safety.txt
```

---

# Overview

The `prompts` package contains all language model prompt templates used by the Multi-Agent Foundry application.

Instead of embedding prompts directly inside Python code, the project stores them as separate text files. This design separates prompt engineering from application logic and allows prompts to evolve independently.

The prompt layer provides instructions that guide the behavior of:

* Planning agents.
* Knowledge retrieval agents.
* Response generation agents.
* Safety validation components.
* Citation formatting.

---

# Prompt Architecture

```text id="p8kw0g"
                 Application
                      │
                      ▼
              Prompt Loader
                      │
        ┌─────────────┼─────────────┐
        ▼             ▼             ▼
    Planner       Knowledge      Response
    Prompt         Prompt        Prompt
        │             │             │
        └─────────────┼─────────────┘
                      │
                      ▼
                 Language Model
```

---

# Benefits of External Prompt Files

## Maintainability

Prompt changes do not require modifications to application code.

---

## Version Control

Prompt changes can be tracked independently.

---

## Experimentation

Different prompt versions can be tested without changing business logic.

---

## Separation of Concerns

Application developers can maintain code while prompt engineers refine instructions.

---

# File: `src/prompts/__init__.py`

## Purpose

Marks the prompts directory as a Python package.

---

## Responsibilities

* Package initialization.
* Optional prompt utility exports.

---

## Dependencies

None.

---

# File: `src/prompts/system.txt`

## Purpose

Defines the global system-level instructions used by the language model.

This prompt establishes the general behavior, role, and constraints of the AI assistant.

---

## Responsibilities

Defines:

* Assistant identity.
* General response behavior.
* Communication style.
* Global safety requirements.
* Output expectations.

---

## Used By

* Response generation.
* Agent execution pipelines.

---

## Typical Content

The system prompt usually contains:

```text
You are an enterprise AI assistant.

Follow organizational policies.

Use available knowledge sources.

Provide accurate and helpful responses.
```

---

# File: `src/prompts/planner.txt`

## Purpose

Defines instructions for the Planner Agent.

The planner prompt guides the model in understanding user intent and creating an execution strategy.

---

## Responsibilities

Helps the model:

* Analyze requests.
* Identify user goals.
* Determine required actions.
* Decide whether retrieval is needed.

---

## Inputs

Typical variables:

* User query.
* Conversation history.
* Available tools.

---

## Outputs

Expected output:

* Task classification.
* Execution plan.
* Query transformation.

---

## Used By

`src/agents/planner.py`

---

# Example Workflow

```text id="l7x5jl"
User Query

↓

Planner Prompt

↓

Language Model

↓

Execution Plan
```

---

# File: `src/prompts/knowledge.txt`

## Purpose

Defines instructions for the Knowledge Agent when interacting with retrieved information.

---

## Responsibilities

Controls:

* Retrieval interpretation.
* Context analysis.
* Information extraction.
* Grounding behavior.

---

## Helps Prevent

* Hallucination.
* Unsupported answers.
* Ignoring retrieved documents.

---

## Inputs

Typical variables:

* User question.
* Retrieved documents.
* Metadata.

---

## Outputs

A structured knowledge response containing relevant information.

---

## Used By

`src/agents/knowledge.py`

---

# File: `src/prompts/query_rewrite.txt`

## Purpose

Provides instructions for improving user queries before retrieval.

Query rewriting improves search accuracy by transforming natural language requests into retrieval-friendly queries.

---

## Responsibilities

* Expand unclear queries.
* Add missing context.
* Remove unnecessary wording.
* Improve search relevance.

---

## Example

Input:

```text
How do I fix access?
```

Possible rewritten query:

```text
Instructions for resolving user access permission issues.
```

---

## Used By

* Planner Agent.
* Knowledge Agent.
* RAG query pipeline.

---

# File: `src/prompts/rag_answer.txt`

## Purpose

Defines instructions for generating final answers using retrieved documents.

This is one of the most important prompts in the application because it controls how the model converts retrieved knowledge into user-facing responses.

---

## Responsibilities

Defines:

* Answer structure.
* Citation behavior.
* Grounding requirements.
* Response style.

---

## Inputs

Typical variables:

* User question.
* Retrieved context.
* Conversation history.
* Citation information.

---

## Outputs

A final user-facing response.

---

## Generation Flow

```text id="1m7h6c"
Question

+

Retrieved Context

+

RAG Prompt

        │

        ▼

Language Model

        │

        ▼

Final Answer
```

---

# File: `src/prompts/citation.txt`

## Purpose

Controls citation generation and formatting behavior.

---

## Responsibilities

Defines:

* Citation format.
* Source references.
* Attribution rules.
* Evidence requirements.

---

## Goals

Ensure responses clearly indicate:

* Where information came from.
* Which documents support the answer.
* What content is based on retrieved evidence.

---

## Used By

* Response Agent.
* RAG citation utilities.

---

# File: `src/prompts/safety.txt`

## Purpose

Defines safety evaluation instructions.

This prompt guides safety checks performed by the Safety Agent.

---

## Responsibilities

Helps identify:

* Unsafe requests.
* Policy violations.
* Prompt injection attempts.
* Restricted content.

---

## Inputs

Typical variables:

* User request.
* Generated response.
* Retrieved information.

---

## Outputs

Safety decision:

```text
ALLOW

or

BLOCK
```

---

## Used By

`src/agents/safety.py`

---

# Prompt Loading Flow

```text id="3v57xq"
Application Startup

        │

        ▼

Prompt Files Loaded

        │

        ▼

Prompt Templates Stored

        │

        ▼

Agents Request Required Prompt

        │

        ▼

Variables Injected

        │

        ▼

Language Model Execution
```

---

# Prompt Engineering Guidelines

## Keep Prompts Focused

Each prompt should have one clear responsibility.

---

## Avoid Business Logic

Prompts should guide model behavior, not replace application code.

---

## Version Prompts

Changes to prompts can significantly affect model behavior and should be tracked.

---

## Test Prompt Changes

Prompt modifications should be evaluated using:

* Existing test cases.
* Evaluation datasets.
* Regression testing.

---

# Module Relationships

| Module              | Relationship                                    |
| ------------------- | ----------------------------------------------- |
| `src/agents/`       | Uses prompts to guide agent behavior.           |
| `src/rag/`          | Uses retrieval-related prompts.                 |
| `src/orchestrator/` | Determines when prompts are executed.           |
| `src/evaluation/`   | Measures prompt effectiveness.                  |
| `src/config/`       | Provides model configuration used with prompts. |
