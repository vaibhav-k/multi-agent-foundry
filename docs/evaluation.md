# Evaluation Module

## Directory Structure

```text id="x8r4pc"
src/
└── evaluation/
    ├── dataset.py
    ├── evaluator.py
    ├── metrics.py
    ├── models.py
    ├── reports.py
    │
    └── samples/
        ├── adversarial_questions.json
        ├── rag_questions.json
        └── security_questions.json
```

---

# Overview

The `evaluation` package provides a framework for measuring the quality, reliability, and safety of the Multi-Agent Foundry application.

AI applications require continuous evaluation because model behavior can change based on:

* Prompt modifications.
* Model updates.
* Retrieval changes.
* Knowledge base changes.
* Configuration updates.

The evaluation module provides repeatable tests that measure system performance against predefined datasets.

---

# Evaluation Architecture

```text id="x4k2m3"
              Evaluation Dataset
                     │
                     ▼
              Dataset Loader
                     │
                     ▼
               Test Questions
                     │
                     ▼
              Application Pipeline
                     │
        ┌────────────┼────────────┐
        ▼            ▼            ▼
    Retrieval    Response     Safety
    Metrics      Metrics     Metrics
        │            │            │
        └────────────┼────────────┘
                     │
                     ▼
              Evaluation Report
```

---

# Evaluation Goals

The framework measures:

## Retrieval Quality

Determines whether the RAG pipeline retrieves useful information.

Metrics include:

* Relevance.
* Precision.
* Recall.
* Context quality.

---

## Response Quality

Measures generated answers.

Metrics include:

* Correctness.
* Grounding.
* Completeness.
* Formatting.

---

## Safety Performance

Measures whether the system properly handles unsafe or restricted requests.

Metrics include:

* Detection accuracy.
* False positives.
* False negatives.

---

# Directory: `src/evaluation/samples/`

## Purpose

Contains predefined evaluation datasets.

These datasets provide standardized questions for testing the AI system.

---

# File: `src/evaluation/dataset.py`

## Purpose

Handles loading and managing evaluation datasets.

---

## Responsibilities

* Load evaluation files.
* Parse question sets.
* Validate dataset structure.
* Provide evaluation samples.

---

## Inputs

Evaluation JSON files.

Example:

```json
{
  "question": "How do I configure MFA?",
  "category": "security"
}
```

---

## Outputs

Structured evaluation cases.

---

## Workflow

```text id="g6y8h3"
JSON Dataset

↓

Dataset Loader

↓

Evaluation Objects

↓

Evaluator
```

---

## Used By

* `evaluator.py`
* Evaluation scripts

---

# File: `src/evaluation/models.py`

## Purpose

Defines data models used by the evaluation framework.

---

## Responsibilities

Represents:

* Evaluation cases.
* Metric results.
* Test outcomes.
* Reports.

---

## Typical Models

### EvaluationCase

Represents a single test question.

Example fields:

```text id="k9l1a2"
EvaluationCase

├── question

├── expected_behavior

├── category

└── metadata
```

---

### EvaluationResult

Stores the outcome of an evaluation run.

Example:

```text id="y6h7z1"
EvaluationResult

├── score

├── metrics

├── response

└── details
```

---

# File: `src/evaluation/evaluator.py`

## Purpose

Executes evaluation workflows against the application.

---

## Responsibilities

* Run test cases.
* Send requests through the AI pipeline.
* Collect responses.
* Calculate metrics.
* Generate evaluation results.

---

## Workflow

```text id="8rj4wq"
Load Dataset

↓

Execute Application

↓

Collect Responses

↓

Calculate Metrics

↓

Generate Results
```

---

## Inputs

* Evaluation dataset.
* Application instance.
* Evaluation configuration.

---

## Outputs

* Evaluation results.
* Metric scores.
* Reports.

---

# File: `src/evaluation/metrics.py`

## Purpose

Defines evaluation metrics used to measure system performance.

---

## Responsibilities

* Calculate quality scores.
* Compare expected and generated outputs.
* Aggregate evaluation statistics.

---

# Retrieval Metrics

Measures the quality of retrieved information.

Examples:

## Relevance Score

Determines whether retrieved documents match the question.

---

## Precision

Measures the percentage of retrieved documents that are useful.

---

## Recall

Measures whether important information was retrieved.

---

# Response Metrics

Measures generated answers.

Examples:

## Grounding

Checks whether the response is supported by retrieved context.

---

## Correctness

Measures whether the answer satisfies the question.

---

## Completeness

Measures whether important details are included.

---

# Safety Metrics

Measures safety behavior.

Examples:

## Detection Rate

How often unsafe requests are correctly identified.

---

## False Positive Rate

Measures incorrectly blocked safe requests.

---

# File: `src/evaluation/reports.py`

## Purpose

Generates human-readable evaluation reports.

---

## Responsibilities

* Format evaluation results.
* Summarize scores.
* Export results.
* Present failures.

---

## Possible Outputs

Formats may include:

* Markdown reports.
* JSON reports.
* Console summaries.

---

## Example Report Structure

```text id="b3j1mx"
Evaluation Summary

Total Tests: 100

Retrieval Score: 92%

Response Score: 89%

Safety Score: 96%

Failures:
- Question 42
- Question 78
```

---

# Evaluation Datasets

## File: `src/evaluation/samples/rag_questions.json`

## Purpose

Contains questions designed to test retrieval and knowledge-grounded responses.

---

## Tests

Examples:

* Document retrieval accuracy.
* Context relevance.
* Answer grounding.

---

# File: `src/evaluation/samples/security_questions.json`

## Purpose

Contains security-focused evaluation cases.

---

## Tests

Examples:

* Access management.
* Authentication.
* Security policies.

---

# File: `src/evaluation/samples/adversarial_questions.json`

## Purpose

Contains challenging prompts designed to test system robustness.

---

## Tests

Examples:

* Prompt injection attempts.
* Ambiguous questions.
* Conflicting instructions.

---

# Evaluation Execution Flow

```text id="5x3v8c"
                 evaluate.py

                      │

                      ▼

             Load Evaluation Dataset

                      │

                      ▼

              Run AI Application

                      │

                      ▼

              Collect Responses

                      │

                      ▼

             Calculate Metrics

                      │

                      ▼

              Generate Report
```

---

# Integration With Other Modules

```text id="g2s7vm"
                Evaluation Module

                       │

      ┌────────────────┼────────────────┐

      ▼                ▼                ▼

    Agents           RAG             API

      │                │                │

      ▼                ▼                ▼

Response Quality  Retrieval Quality  End-to-End Tests
```

---

# Best Practices

## Maintain Evaluation Datasets

Evaluation data should evolve with:

* New features.
* New documents.
* New attack patterns.

---

## Run Regression Tests

Evaluation should run after:

* Prompt changes.
* Model upgrades.
* Retrieval changes.

---

## Track Metrics Over Time

Store historical results to identify quality improvements or regressions.

---

## Include Edge Cases

Datasets should contain:

* Normal questions.
* Difficult questions.
* Safety-sensitive requests.
* Ambiguous queries.

---

# Module Relationships

| Module                | Relationship                                   |
| --------------------- | ---------------------------------------------- |
| `src/rag/`            | Provides retrieval quality evaluation targets. |
| `src/agents/`         | Evaluates agent behavior.                      |
| `src/api/`            | Supports end-to-end API testing.               |
| `src/orchestrator/`   | Evaluates workflow execution.                  |
| `scripts/evaluate.py` | Provides command-line evaluation entry point.  |
