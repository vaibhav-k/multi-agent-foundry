# File Reference

This section documents every file in the project. Each file includes its purpose, responsibilities, dependencies, expected inputs and outputs, and how it fits into the overall system.

---

# Root Files

---

# `/.env`

## Purpose

Stores environment-specific configuration values required to run the application.

This file is **not committed** to source control because it contains secrets such as API keys and service endpoints.

---

## Typical Contents

```env
AZURE_OPENAI_ENDPOINT=
AZURE_OPENAI_API_KEY=
AZURE_OPENAI_DEPLOYMENT=
AZURE_OPENAI_EMBEDDING_DEPLOYMENT=

LOG_LEVEL=INFO
```

---

## Used By

- `src/config/settings.py`
- `src/config/client.py`
- `src/bootstrap.py`

---

## Responsibilities

- Store API credentials
- Configure Azure services
- Configure logging
- Store deployment settings

---

## Notes

Never commit this file to Git.

---

# `/.env.example`

## Purpose

Template showing the required environment variables.

Unlike `.env`, this file contains **placeholder values** and is safe to commit.

---

## Responsibilities

- Documents required variables
- Helps new developers configure the project
- Prevents missing configuration

---

## Example

```env
AZURE_OPENAI_ENDPOINT=
AZURE_OPENAI_API_KEY=
AZURE_OPENAI_DEPLOYMENT=
```

---

# `/.gitignore`

## Purpose

Defines files and directories excluded from version control.

---

## Common Entries

```
.env
__pycache__/
.pytest_cache/
.venv/
*.pyc
```

---

## Responsibilities

- Ignore secrets
- Ignore generated files
- Ignore cache
- Ignore virtual environments

---

# `/README.md`

## Purpose

Primary project documentation.

Provides:

- Overview
- Installation
- Architecture
- Usage
- Developer guide

---

# `/requirements.txt`

## Purpose

Lists all Python dependencies required to run the project.

---

## Responsibilities

Ensures reproducible environments.

Example installation:

```bash
pip install -r requirements.txt
```

---

## Typical Dependencies

- fastapi
- uvicorn
- openai
- pytest
- python-dotenv
- pydantic

---

# `/pytest.ini`

## Purpose

Configuration file for pytest.

---

## Responsibilities

- Configure test discovery
- Configure markers
- Configure output
- Configure warnings

---

Example

```ini
[pytest]
testpaths = tests
python_files = test_*.py
```

---

# `/scripts/evaluate.py`

## Purpose

Entry point for evaluation.

Runs benchmark datasets against the application.

---

## Responsibilities

- Load datasets
- Execute evaluation
- Collect metrics
- Generate reports

---

## Used By

Developers during model evaluation.

---

## Typical Workflow

```
Dataset

↓

Retriever

↓

LLM

↓

Metrics

↓

Report
```

---

# Source Directory

---

# `/src/__init__.py`

## Purpose

Marks `src` as a Python package.

Usually contains minimal initialization logic.

---

# `/src/bootstrap.py`

## Purpose

Application bootstrapper.

Responsible for preparing the runtime before the application starts.

---

## Responsibilities

- Load environment variables
- Initialize logging
- Create Azure client
- Validate configuration
- Register services

---

## Used By

- `main.py`
- API startup

---

## Dependencies

- `config/settings.py`
- `config/client.py`
- `config/logger.py`

---

## Startup Flow

```
Load .env

↓

Load settings

↓

Initialize logging

↓

Create Azure client

↓

Validate configuration

↓

Return initialized application
```

---

# `/src/main.py`

## Purpose

Main application entry point.

Responsible for launching the system.

---

## Responsibilities

- Bootstrap application
- Start API
- Initialize orchestrator
- Register startup events

---

## Execution

```bash
python -m src.main
```

---

## Typical Flow

```
main()

↓

bootstrap()

↓

Create API

↓

Start server
```

---

# `/src/models.py`

## Purpose

Contains shared application models.

These models are reused throughout multiple modules.

---

## Responsibilities

- Shared request models
- Shared response models
- Domain objects
- Common data structures

---

## Used By

- agents
- orchestrator
- memory
- rag
- api

---

## Advantages

Centralizing models avoids duplicated definitions across the project.

---

# Directory Overview

The remaining documentation covers every directory individually.

Upcoming sections include:

- `src/agents/`
- `src/api/`
- `src/config/`
- `src/evaluation/`
- `src/memory/`
- `src/orchestrator/`
- `src/prompts/`
- `src/rag/`
- `src/state/`
- `src/utils/`

Each Python file will be documented with:

- Purpose
- Responsibilities
- Dependencies
- Inputs
- Outputs
- Classes
- Functions
- Workflow
- Integration with the rest of the system